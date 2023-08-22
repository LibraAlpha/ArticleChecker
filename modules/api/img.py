import os
import os.path
import shutil

from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse

from configs.basics import get_root_path
from modules.ftp_tools import upload
from modules.db.redis_tools import append
from modules.Asset import Asset
from modules.db import mysql_tools

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
        return JSONResponse(content={f'message': '上传失败:{e}'}, status_code=500)


@router.get('/api/img/replace_url')
async def replace_url(asset_id: int, original_url: str, target_url: str):
    # 记录链接变化情况
    ret = append(original_url, target_url)

    session = mysql_tools.Session()

    data_to_update = session.query(Asset).filter(Asset.id == asset_id).all()
    try:
        for asset_item in data_to_update:
            asset_item.url_replaced = target_url.strip("")
        session.commit()
    except Exception as e:
        ret = 0
    finally:
        session.close()

    if ret == 1:
        return JSONResponse(content={'message': '已成功替换'})
    else:
        return JSONResponse(content={'message': '数据写入redis发生问题'})
