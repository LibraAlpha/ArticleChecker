import os
import os.path
import shutil

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from configs.basics import get_root_path
from modules.ftp_tools import upload

router = APIRouter()

UPLOAD_DIR = f'{get_root_path()}/tmp'


@router.post('/api/img/upload')
async def upload(orignal_file_name, file: UploadFile = File(...)):
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        # @TODO:通过接口获取原始文件名称
        upload_ret = upload(orignal_file_name, file_path)
        return JSONResponse(content={'message': '上传成功', 'url': file_path})
    except Exception as e:
        return JSONResponse(content={'message': '上传失败'}, status_code=500)
