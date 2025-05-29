from pathlib import Path
import feedparser
import csv
import schedule
import time

from definitions import EXTERNAL_DATA_FOLDER, FETCH_PERIOD_HOURS, RSS_FEEDS


def fetch_rss_feeds(feeds: list[str], path: Path):
    all_entries = []
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            all_entries.append(
                {
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", "Unknown"),
                    "source": url,
                }
            )

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "a") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "link", "published", "source"])
        writer.writeheader()
        writer.writerows(all_entries)


def fetch_rss_feeds_default():
    fetch_rss_feeds(RSS_FEEDS, EXTERNAL_DATA_FOLDER / "rss_feed.csv")


if __name__ == "__main__":
    fetch_rss_feeds_default()
    schedule.every(FETCH_PERIOD_HOURS).hours.do(fetch_rss_feeds_default)
    while True:
        schedule.run_pending()
        time.sleep(60)
