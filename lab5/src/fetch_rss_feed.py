import feedparser
import schedule
import time
from dateutil import parser

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from definitions import (
    ES_HOST,
    ES_PASSWORD,
    ES_USERNAME,
    INDEX_NAME,
    EXTERNAL_DATA_FOLDER,
    FETCH_PERIOD_HOURS,
    RSS_FEEDS,
)


def fetch_rss_feeds(feeds: list[str]):
    all_entries = []
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            raw_date = entry.get("published")
            try:
                published = parser.parse(raw_date).isoformat() if raw_date else None
            except Exception:
                published = None

            all_entries.append(
                {
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", "Unknown"),
                    "source": url,
                }
            )

    actions = [{"_index": INDEX_NAME, "_source": doc} for doc in all_entries]

    es = Elasticsearch(
        [ES_HOST], basic_auth=(ES_USERNAME, ES_PASSWORD), verify_certs=False
    )

    bulk(es, actions)


def fetch_rss_feeds_default():
    fetch_rss_feeds(RSS_FEEDS)


if __name__ == "__main__":
    fetch_rss_feeds_default()
    schedule.every(FETCH_PERIOD_HOURS).hours.do(fetch_rss_feeds_default)
    while True:
        schedule.run_pending()
        time.sleep(60)
