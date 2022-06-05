import os
from fastapi import FastAPI
from mangum import Mangum


STAGE = os.environ.get('STAGE')
root_path = '/' if not STAGE else f'/{STAGE}'
app = FastAPI(title="FastAPI x AWS Lambda", root_path=root_path)


@app.get("/hi")
def hello_world():
    return {"message": "Hello World"}


handler = Mangum(app)
