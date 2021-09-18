from datetime import datetime, timedelta

from base.celery import app
from celery.utils.log import get_task_logger

from apps.twitter.adapter import TwitterAdapter
from apps.twitter.models import Tag

logger = get_task_logger(__name__)


@app.task(
    name="get_tweets",
    ignore_result=True,
)
def get_tweets():
    logger.info("start to fetch data.")

    # get tags
    tags_qs = Tag.objects.filter(get_data=True)

    yesterday = datetime.now() - timedelta(1)

    try:
        for tag in tags_qs:
            # get data
            logger.info(f"start to fetch tag: {tag.slug}")
            TwitterAdapter().get_tweets(
                tag.tag,
                tag.lang,
                datetime.strftime(yesterday, "%Y-%m-%d"),
                tag.collect_size,
            )
    except Exception as e:
        logger.error("error in fetching data from twitter.", e)

    logger.info("fetching data finished.")
