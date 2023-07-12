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

from secrets import compare_digest

from PIL import PngImagePlugin, Image

from modules.api import sens_words, article,ad_pos

app = FastAPI()

app.include_router(sens_words.router)
app.include_router(article.router)
app.include_router(ad_pos.router)


def create_api():
    return app
