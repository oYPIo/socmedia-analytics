import json
from elasticsearch import Elasticsearch
from definitions import (
    ES_PASSWORD,
    ES_USERNAME,
    ES_HOST,
    INDEX_NAME,
    EXTERNAL_DATA_FOLDER,
)


def generate_batch_json(index, data, output_file):
    if output_file.exists():
        return output_file

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        for it in data:
            file.write(json.dumps({"index": {"_index": index}}) + "\n")
            file.write(json.dumps(it) + "\n")

    return output_file


def upload_to_elasticsearch(bulk_file, es_host):
    es = Elasticsearch(
        [es_host], basic_auth=(ES_USERNAME, ES_PASSWORD), verify_certs=False
    )
    with open(bulk_file, "r", encoding="utf-8") as file:
        bulk_data = file.read()
    response = es.bulk(body=bulk_data)
    print("Elasticsearch response:", response)


if __name__ == "__main__":
    data = [
        {"id": 1, "name": "Item 1", "value": 100},
        {"id": 2, "name": "Item 2", "value": 200},
        {"id": 3, "name": "Item 3", "value": 300},
    ]
    bulk_file = EXTERNAL_DATA_FOLDER / "bulk-data.txt"

    generate_batch_json(INDEX_NAME, data, bulk_file)
    upload_to_elasticsearch(bulk_file, ES_HOST)
