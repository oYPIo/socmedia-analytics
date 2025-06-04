from pathlib import Path


PROJECT_ROOT_DIR = Path(__file__).parent.parent.absolute()

EXTERNAL_DATA_FOLDER = PROJECT_ROOT_DIR / "data" / "external"


ES_USERNAME = "elastic"
ES_PASSWORD = "changeme"
ES_HOST = "http://localhost:9200"
INDEX_NAME = "test"
