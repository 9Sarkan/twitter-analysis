import collections
import itertools
import os
import re

from nltk.corpus import stopwords


def get_env(name, default=None, raise_exception=False):
    value = os.environ.get(name, default)
    if not value and raise_exception:
        raise Exception(f"You must set {name} variable in your env")
    return value


class Helper(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = super(Helper, cls).__new__(Helper, *args, **kwargs)
        return cls.__instance

    def remove_url(self, text):
        """
        Replace URLs found in a text string with nothing
        (i.e. it will remove the URL from the string).

        Parameters
        ----------
        text : string
            A text string that you want to parse and remove urls.

        Returns
        -------
        The same text string with url's removed.
        """

        return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", text).split())

    def get_list_of_all_words(self, words_in_tweet):
        return itertools.chain(*words_in_tweet)

    def get_counter(self, all_words, most_common):
        counts = collections.Counter(all_words)
        return counts.most_common(most_common)

    def get_stop_words(self, lang):
        stop_words = set(stopwords.words(lang))

        ################################################################
        stw = [
            "i",
            "its",
            "again",
            "having",
            "our",
            "after",
            "should've",
            "by",
            "at",
            "hasn't",
            "nor",
            "their",
            "they",
            "these",
            "in",
            "more",
            "wasn't",
            "that'll",
            "such",
            "during",
            "be",
            "t",
            "what",
            "ll",
            "for",
            "until",
            "doesn",
            "his",
            "didn",
            "couldn",
            "both",
            "most",
            "won't",
            "no",
            "shouldn't",
            "below",
            "theirs",
            "can",
            "me",
            "a",
            "haven't",
            "out",
            "yourself",
            "mightn",
            "we",
            "and",
            "mustn",
            "haven",
            "them",
            "where",
            "hadn",
            "just",
            "because",
            "wouldn't",
            "themselves",
            "doing",
            "aren",
            "that",
            "as",
            "those",
            "on",
            "will",
            "him",
            "who",
            "between",
            "hadn't",
            "not",
            "weren",
            "m",
            "shan't",
            "any",
            "with",
            "same",
            "which",
            "other",
            "through",
            "she's",
            "needn",
            "you",
            "aren't",
            "how",
            "did",
            "had",
            "you'd",
            "ain",
            "d",
            "you've",
            "down",
            "needn't",
            "why",
            "off",
            "but",
            "this",
            "against",
            "here",
            "own",
            "ma",
            "himself",
            "the",
            "were",
            "it's",
            "yourselves",
            "once",
            "been",
            "ours",
            "wasn",
            "than",
            "up",
            "s",
            "couldn't",
            "itself",
            "ve",
            "you'll",
            "is",
            "has",
            "should",
            "over",
            "weren't",
            "he",
            "about",
            "into",
            "do",
            "to",
            "under",
            "didn't",
            "re",
            "don't",
            "won",
            "or",
            "while",
            "does",
            "too",
            "o",
            "of",
            "if",
            "from",
            "isn",
            "mightn't",
            "mustn't",
            "you're",
            "very",
            "it",
            "further",
            "so",
            "y",
            "being",
            "whom",
            "are",
            "ourselves",
            "each",
            "an",
            "herself",
            "your",
            "some",
            "there",
            "before",
            "few",
            "shouldn",
            "all",
            "my",
            "isn't",
            "only",
            "don",
            "am",
            "then",
            "was",
            "myself",
            "shan",
            "she",
            "have",
            "now",
            "when",
            "above",
            "hers",
            "doesn't",
            "wouldn",
            "hasn",
            "her",
            "yours",
        ]
        return stop_words

    def remove_stop_words(self, words_in_tweet, stop_words):
        tweets_nsw = [word for word in words_in_tweet if not word in stop_words]
        return tweets_nsw

    def remove_collection_words(self, words_in_tweet, collection_words):
        return [w for w in words_in_tweet if not w in collection_words]
