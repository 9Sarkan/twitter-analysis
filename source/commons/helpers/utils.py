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
            cls.__instance = super(Helper, cls).__new__(
                Helper, *args, **kwargs)
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
        return stop_words

    def remove_stop_words(self, words_in_tweet, stop_words):
        tweets_nsw = [
            word for word in words_in_tweet if not word in stop_words]
        return tweets_nsw

    def remove_collection_words(self, words_in_tweet, collection_words):
        return [w for w in words_in_tweet if not w in collection_words]
