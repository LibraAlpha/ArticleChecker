import os.path
import os
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import shutil

router = APIRouter()

UPLOAD_DIR = './uploads'


@router.post('/api/img/upload')
async def upload(file: UploadFile = File(...)):
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        return JSONResponse(content={'message': '上传成功', 'url': file_path})
    except Exception as e:
        return JSONResponse(content={'message': '上传失败'}, status_code=500)

