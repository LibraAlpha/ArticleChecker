from fastapi import APIRouter
from modules.db import mysql_tools, redis_tools
from modules.Asset import Asset
from sqlalchemy import or_

router = APIRouter()


@router.get('/api/assets/list')
def get_articles(date: str, page_index: int, page_limit: int):
    page_offset = (page_index - 1) * page_limit

    session = mysql_tools.Session()

    query = session.query(Asset).filter(Asset.created_at == date).order_by(Asset.created_at.desc())

    total_count = query.count()

    query = query.limit(page_limit)

    query = query.offset(page_offset)

    assets = query.all()

    assets_data = []

    for asset in assets:
        asset_data = {
            'id': asset.id,
            'url': asset.url,
            'title': asset.title,
            'desc': asset.asset_desc,
            'adv': asset.adv,
            'is_checked': asset.is_checked,
            'sensitive_words': asset.sensitive_words,
            'adpos': asset.ad_pos,
            'url_replaced': asset.url_replaced,
            'video_url': asset.video_url,
            'bid': asset.bid,
            'impression': asset.impression,
            'click': asset.click
        }
        assets_data.append(asset_data)

    return {"total_count": total_count, 'info': assets_data}


@router.get('/api/assets/find')
def find_articles(date: str, page_index: int, page_limit: int, adv: str, keywords: str):
    page_offset = (page_index - 1) * page_limit

    session = mysql_tools.Session()

    if keywords == '*':
        query = session.query(Asset) \
            .filter(Asset.created_at == date) \
            .filter(Asset.adv == adv) \
            .order_by(Asset.created_at.desc())
    else:
        query = session.query(Asset) \
            .filter(Asset.created_at == date) \
            .filter(Asset.adv == adv) \
            .filter(or_(Asset.title.like(f'%{keywords}%'), Asset.asset_desc.like(f'%{keywords}%'))) \
            .order_by(Asset.created_at.desc())

    total_count = query.count()

    query = query.limit(page_limit)
    query = query.offset(page_offset)

    assets = query.all()

    assets_data = []

    for asset in assets:
        asset_data = {
            'url': asset.url,
            'title': asset.title,
            'desc': asset.asset_desc,
            'adv': asset.adv,
            'is_checked': asset.is_checked,
            'created_at': asset.created_at,
            'id': asset.id,
            'sensitive_words': asset.sensitive_words
        }
        assets_data.append(asset_data)

    return {"total_count": total_count, 'info': assets_data}


@router.get('/api/assets/blacklist')
def get_black_list(date: str, page_index: int, page_limit: int, adv: str):
    page_offset = (page_index - 1) * page_limit

    session = mysql_tools.Session()

    if keywords == '*':
        query = session.query(Asset) \
            .filter(Asset.created_at == date) \
            .filter(Asset.adv == adv) \
            .filter(Asset.is_sensitive is True) \
            .order_by(Asset.created_at.desc())
    else:
        query = session.query(Asset) \
            .filter(Asset.created_at == date) \
            .filter(Asset.adv == adv) \
            .filter(Asset.is_sensitive is True) \
            .filter(or_(Asset.title.like(f'%{keywords}%'), Asset.asset_desc.like(f'%{keywords}%'))) \
            .order_by(Asset.created_at.desc())

    total_count = query.count()

    query = query.limit(page_limit)
    query = query.offset(page_offset)

    assets = query.all()

    assets_data = []

    for asset in assets:
        asset_data = {
            'url': asset.url,
            'title': asset.title,
            'desc': asset.asset_desc,
            'adv': asset.adv,
            'is_checked': asset.is_checked,
            'created_at': asset.created_at,
            'id': asset.id,
            'sensitive_words': asset.sensitive_words,
            'adpos': asset.ad_pos
        }
        assets_data.append(asset_data)

    return {"total_count": total_count, 'info': assets_data}


@router.put('/api/assets/blacklist/add')
def add_to_blacklist(id: int):
    return
