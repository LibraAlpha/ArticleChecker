from fastapi import APIRouter
from modules import adpos_tools
from modules.db import mysql_tools
from modules.AdPos import AdPosInfo, AdPos

router = APIRouter()


# 广告位管理接口部分
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


# 广告位信息部分
@router.get('/api/adpos/info')
async def load(date):
    session = mysql_tools.Session()
    query = session.query(AdPos).filter(AdPos.dt == date).order_by(AdPos.bid.desc(), AdPos.name.asc())

    total_count = query.count()

    query_results = query.all()

    results = []

    for adpos in query_results:
        info_data = {
            'id': adpos.id,
            'name': adpos.name,
            'bid': adpos.bid,
            'impression': adpos.impression,
            'click': adpos.click
        }
        results.append(info_data)

    return {'total_count': total_count, 'info': results}
