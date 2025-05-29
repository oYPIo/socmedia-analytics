import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from definitions import (
    ES_HOST,
    ES_USERNAME,
    ES_PASSWORD,
    INDEX_NAME,
    CONTENT_FOLDER,
)

app = FastAPI()
es = Elasticsearch([ES_HOST], basic_auth=(ES_USERNAME, ES_PASSWORD), verify_certs=False)


@app.get("/", response_class=HTMLResponse)
async def upload_page():
    with open(CONTENT_FOLDER / "upload.html", "r") as file:
        return file.read()


@app.post("/upload/")
async def upload_json(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        data = json.loads(contents.decode("utf-8"))

        if not isinstance(data, list):
            raise HTTPException(
                status_code=400, detail="JSON має бути списком об'єктів"
            )

        actions = [{"_index": INDEX_NAME, "_source": doc} for doc in data]
        bulk(es, actions)

        return {
            "message": "Файл успішно завантажено в Elasticsearch",
            "count": len(data),
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Некоректний JSON")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
