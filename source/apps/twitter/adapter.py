import os
import json
import time

import nltk
import tweepy
from base.interfaces.redis import Client as RedisClient
from commons.helpers.utils import Helper
from django.conf import settings
from .documents import TweetsDocument
import requests


class TwitterAdapter(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TwitterAdapter, cls).__new__(
                TwitterAdapter, *args, **kwargs
            )
        return cls._instance

    def __init__(self):
        self._api_key = settings.TWITTER_API_KEY
        self._api_key_secret = settings.TWITTER_API_SECRET_KEY
        self._access_token = settings.TWITTER_ACCESS_TOKEN
        self._access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
        self._auth = tweepy.OAuthHandler(self._api_key, self._api_key_secret)
        self.api = tweepy.API(self._auth, wait_on_rate_limit=True)

    def search(self, search_terms, lang, since, items, collection, most_common):
        helper = Helper()

        all_tweets = self.get_tweets(search_terms, lang, since, items)
        if len(all_tweets) == 0:
            return []

        return self.get_most_common(search_terms, collection, most_common)

    def get_most_common(self, tag, collection, most_common):
        stop_words = Helper().get_stop_words("english")

        query_map = {
            "query": {
                "match": {
                    "search_item": tag,
                }
            },
            "aggs": {
                "mostUsed": {
                    "terms": {
                        "field": "text.keyword",
                        "exclude": ["rt", *stop_words, *collection],
                        "size": most_common,
                    }
                }
            },
        }

        marshaled_data = json.dumps(query_map)

        headers = {
            "Content-Type": "application/json",
        }

        response = requests.post(
            f'http://{settings.ELASTICSEARCH_DSL["default"]["hosts"]}/tweets/_search',
            headers=headers,
            data=marshaled_data,
        )

        return response.json()["aggregations"]["mostUsed"]["buckets"]

    def get_tweets(self, search_terms, lang, since, items):
        tweets = tweepy.Cursor(
            self.api.search,
            q=search_terms,
            lang=lang,
            since=since,
            tweet_mode="extended",
        ).items(items)
        for t in tweets:
            TweetsDocument(
                id=t.id,
                lang=t.lang,
                author=t.author.__dict__["_json"],
                entities=t.entities,
                search_item=search_terms,
                source=t.source,
                text=self.convert_to_list(t.full_text),
                raw_text=t.full_text,
                retweet_count=t.retweet_count,
            ).save()

    def convert_to_list(self, tweet):
        """
        Split the words from one tweet into unique elements
        """
        return tweet.lower().split(" ")

    def get_from_populars(self, tag, limit):
        """
        get tweets from most populars
        """
        query_map = {
            "query": {"match": {"search_item": tag}},
            "_source": [
                "author.name",
                "author.followers_count",
                "author.profile_background_image_url",
                "author.description",
                "raw_text",
                "entities.hashtags.text",
            ],
            "sort": [{"author.followers_count": {"order": "desc"}}],
            "size": limit,
        }
        marshaled_data = json.dumps(query_map)
        headers = {
            "Content-Type": "application/json",
        }
        response = requests.post(
            f'http://{settings.ELASTICSEARCH_DSL["default"]["hosts"]}/tweets/_search?filter_path=hits.hits._source',
            headers=headers,
            data=marshaled_data,
        )
        return response.json()["hits"]["hits"]

    def get_most_retweet(self, tag, limit):
        """
        get tweets sorted by most retweeted
        """

        query_map = {
            "query": {"match": {"search_item": tag}},
            "_source": [
                "author.name",
                "author.followers_count",
                "author.profile_background_image_url",
                "author.description",
                "raw_text",
                "entities.hashtags.text",
            ],
            "sort": [{"retweet_count": {"order": "desc"}}],
            "size": limit,
        }
        marshaled_data = json.dumps(query_map)
        headers = {
            "Content-Type": "application/json",
        }
        response = requests.post(
            f'http://{settings.ELASTICSEARCH_DSL["default"]["hosts"]}/tweets/_search?filter_path=hits.hits._source',
            headers=headers,
            data=marshaled_data,
        )
        return response.json()["hits"]["hits"]
