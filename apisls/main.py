import os
import time
from fastapi import FastAPI, Request
from mangum import Mangum
from enum import Enum
from apisls.database.db_utils import create_plant, get_plant_list
from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.core.models import http
from apisls.logger import logger

from aws_lambda_powertools import Tracer

tracer = Tracer()


class Language(str, Enum):
    french = "fr"
    english = "en"
    russian = "ru"


STAGE = os.environ.get('STAGE')
root_path = '/' if not STAGE else f'/{STAGE}'
app = FastAPI(title="FastAPI x AWS Lambda", root_path=root_path)


@app.get("/hi")
def hello_world():
    return {"message": "Hello World"}


@app.put("/plant/{name}")
def add_plant(name: str):
    tracer.put_annotation("add_plant", name)
    create_plant(name)


@app.get("/plants")
def get_plants():
    return get_plant_list()


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/languages/")
async def get_langs():
    return [x[0] for x in Language.__members__.items()]


@app.get("/languages/{lang}")
async def get_lang(lang: Language):
    if lang == Language.french:
        return {"lang": lang, "message": "Je parle français"}
    if lang == Language.english:
        return {"lang": lang, "message": "I speak English"}
    if lang == Language.russian:
        return {"lang": lang, "message": "Я говорю по-русски"}


handler = Mangum(app)
handler.__name__ = "plants_api_handler"
handler = tracer.capture_lambda_handler(handler)
patch_all()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    subsegment_name = str(request.url).replace(str(request.base_url), "")
    with xray_recorder.in_subsegment(subsegment_name) as subsegment:
        subsegment.put_http_meta(http.URL, str(request.url))
        subsegment.put_http_meta(http.METHOD, request.method)
        tracer.put_annotation("endpoint", subsegment_name)


        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
    return response
