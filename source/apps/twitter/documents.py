from django_elasticsearch_dsl import Document, fields, Index
from . import models

tweet_index = Index("tweets")

tweet_index.settings(number_of_shards=1, number_of_replicas=0)


@tweet_index.doc_type
class TweetsDocument(Document):
    # search_item = fields.TextField(attrs="search_item")
    excepted_words = fields.ListField(field=fields.TextField)

    author = fields.ObjectField()
    entities = fields.ObjectField()
    text = fields.TextField(
        fields={"raw": fields.KeywordField()}, analyzer="text_analyser"
    )
    raw_text = fields.TextField()

    retweet_count = fields.IntegerField()

    class Django:
        model = models.Tweet
        fields = [
            "search_item",
            "id",
            # "author",
            "created_date",
            # "entities",
            "source",
            "lang",
        ]

        auto_refresh = False
        ignore_signals = False
        # Paginate the django queryset used to populate the index with the specified size (by
        # default there is no pagination)
        queryset_pagination = 1000
