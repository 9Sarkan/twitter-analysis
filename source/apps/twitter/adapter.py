import os
import time

import nltk
import tweepy
from base.interfaces.redis import Client as RedisClient
from commons.helpers.utils import Helper
from django.conf import settings


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

        ttt0 = time.time()
        all_tweets = self.get_tweets(search_terms, lang, since, items)
        if len(all_tweets) == 0:
            return []

        tt0 = time.time()
        tweets_without_urls = self.remove_url(all_tweets)

        tg0 = time.time()
        list_of_tweet_words = [
            self.convert_to_list(tweet) for tweet in tweets_without_urls
        ]
        list_of_all_words = helper.get_list_of_all_words(list_of_tweet_words)

        # TODO: use ID
        tag_for_redis = search_terms.split()[0]
        # save in redis
        t0 = time.time()
        self.save_on_redis(list_of_all_words, tag_for_redis)
        # get top 10 and remove stop words if exists
        return self.get_most_common(tag_for_redis, collection, most_common)

    def get_most_common(self, tag, collection, most_common):
        stop_words = Helper().get_stop_words("english")
        while True:
            top_ten = RedisClient().get_most_common(tag, most_common)
            for word in top_ten:
                if (
                    word.decode("utf-8") in stop_words
                    or word.decode("utf-8") in collection
                ):
                    RedisClient().remove_from_list(tag, word)
                    top_ten.remove(word)
            if len(top_ten) == most_common:
                break
        return top_ten

    def get_tweets(self, search_terms, lang, since, items):
        tweets = tweepy.Cursor(
            self.api.search, q=search_terms, lang=lang, since=since
        ).items(items)
        return [tweet.text for tweet in tweets]

    def remove_url(self, tweets):
        return [Helper().remove_url(tweet) for tweet in tweets]

    def convert_to_list(self, tweet):
        """
        Split the words from one tweet into unique elements
        """
        return tweet.lower().split()

    def save_on_redis(self, tweets, search_terms):
        client = RedisClient()
        for word in tweets:
            client.add_to_list(search_terms, word)
