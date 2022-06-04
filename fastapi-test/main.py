from typing import Union
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel


class Language(str, Enum):
    french = "fr"
    english = "en"
    russian = "ru"


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


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