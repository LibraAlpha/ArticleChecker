from fastapi import APIRouter
from modules import adpos_tools

router = APIRouter()


@router.get('/api/adpos/list')
def get_adpos_list(page_index: int, page_limit):
    return adpos_tools.load(page_index, page_limit)


@router.put('/api/adpos/add')
def add(name):
    return adpos_tools.add(name)


@router.delete('/api/adpos/del')
def delete(name):
    return adpos_tools.remove(name)


@router.get('/api/adpos/size')
def get_table_size():
    return adpos_tools.get_size()
