from fastapi import APIRouter
from modules import adpos_tools

router = APIRouter()


@router.get('/api/adpos/list')
async def get_adpos_list(page_index: int, page_limit: int):
    ret = adpos_tools.load(page_index, page_limit)
    return ret


@router.put('/api/adpos/add')
async def add(name: str):
    ret = adpos_tools.add(name)
    return ret


@router.delete('/api/adpos/del')
async def delete(name: str):
    return adpos_tools.remove(name)


@router.get('/api/adpos/size')
async def get_table_size():
    return adpos_tools.get_size()
