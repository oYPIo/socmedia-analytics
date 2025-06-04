from pathlib import Path


PROJECT_ROOT_DIR = Path(__file__).parent.parent.absolute()

EXTERNAL_DATA_FOLDER = PROJECT_ROOT_DIR / "data" / "external"
RAW_DATA_FOLDER = PROJECT_ROOT_DIR / "data" / "raw"
PROCESSED_DATA_FOLDER = PROJECT_ROOT_DIR / "data" / "processed"

RSS_FEEDS = [
    "https://www.wired.com/feed/rss",
    "https://rss.slashdot.org/Slashdot/slashdot",
    "https://www.theverge.com/rss/index.xml",
]

FETCH_PERIOD_HOURS = 1/(60*20)

ES_USERNAME = "elastic"
ES_PASSWORD = "changeme"
ES_HOST = "http://localhost:9200"
INDEX_NAME = "test"
