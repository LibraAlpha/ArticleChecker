import base64
import io
import time
import datetime
import uvicorn
import gradio as gr
from threading import Lock
from io import BytesIO
from fastapi import APIRouter, Depends, FastAPI, Request, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from secrets import compare_digest

from PIL import PngImagePlugin, Image

from modules.api import sens_words, asset, ad_pos, img, auth

app = FastAPI()

app.include_router(sens_words.router)
app.include_router(asset.router)
app.include_router(ad_pos.router)
app.include_router(img.router)
app.include_router(auth.router)


origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_api():
    return app


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8668)
