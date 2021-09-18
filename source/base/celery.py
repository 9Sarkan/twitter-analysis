import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")

app = Celery("base")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):

    from apps.twitter.tasks import get_tweets
    from django.conf import settings

    get_tweets()

    sender.add_periodic_task(
        settings.TAGS_UPDATE_PERIOD,
        get_tweets.s(),
        name="get tweets scheduler",
    )
