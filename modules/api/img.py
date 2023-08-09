import os
import os.path
import shutil

from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse

from configs.basics import get_root_path
from modules.ftp_tools import upload

router = APIRouter()

UPLOAD_DIR = f'{get_root_path()}/tmp'


@router.post('/api/img/upload')
async def upload_img2cdn(file: UploadFile = File(...), original_file_name: str = Form(...)):
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        upload_ret = upload(original_file_name, file_path)
        return JSONResponse(content={'message': '上传成功', 'url': upload_ret})
    except Exception as e:
        return JSONResponse(content={'message': '上传失败'}, status_code=500)


@router.get('/api/img/replace')
async def replace_url(original_url: str, target_url: str):
    return JSONResponse(content={'message': '已成功替换'})
