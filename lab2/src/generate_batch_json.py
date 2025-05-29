import json
from pathlib import Path
from definitions import EXTERNAL_DATA_FOLDER


def generate_batch_json(data, output_file: Path):
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump({"batch": data}, file)


if __name__ == "__main__":
    data = [
        {"id": 1, "name": "Item 1", "value": 100},
        {"id": 2, "name": "Item 2", "value": 200},
        {"id": 3, "name": "Item 3", "value": 300},
    ]
    generate_batch_json(data, EXTERNAL_DATA_FOLDER / "example.json")