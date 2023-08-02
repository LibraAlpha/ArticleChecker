import logging
from modules.db import mysql_tools
from modules.AdPos import AdPos, AdPosInfo
from sqlalchemy import distinct, func
from configs import action_code

# 广告位信息管理部分

def load(page_index, page_limit):
    page_offset = (page_index - 1) * page_limit

    session = mysql_tools.Session()

    query = session.query(AdPosInfo)

    total_count = query.count()

    # 执行查询语句
    query = query.limit(page_limit)
    query = query.offset(page_offset)

    data_all = query.all()

    adpos_data_collection = []

    for adpos in data_all:
        adpos_data = {
            'id': adpos.id,
            'name': adpos.name,
        }
        adpos_data_collection.append(adpos_data)

    return {"total_count": total_count, 'info': adpos_data_collection}


def load_all_adpos():
    session = mysql_tools.Session()
    query = session.query(distinct(AdPosInfo.name))

    total_count = query.count()

    adpos_all = query.all()

    adpos_data_collection = []

    for adpos in adpos_all:
        adpos_data = {
            'name': adpos.name,
            'id': adpos.id
        }
        adpos_data_collection.append(adpos_data)

    return {"total_count": total_count, 'info': adpos_data_collection}


def remove(adpos):
    session = mysql_tools.Session()

    data_to_delete = session.query(AdPosInfo).filter_by(name=adpos).first()

    if data_to_delete:
        session.delete(data_to_delete)
        session.commit()

    return


def find(adpos):
    session = mysql_tools.Session()

    query = session.query(AdPosInfo).filter(AdPosInfo.name.like(f'%{adpos}%'))

    total_count = query.count()

    data_all = query.all()

    for adpos in data_all:
        adpos_data = {
            'id': adpos.id,
            'name': adpos.name
        }
        adpos_data_collection.append(adpos_data)

    return {"total_count": total_count, 'info': adpos_data_collection}


def add(adpos):
    session = mysql_tools.Session()

    new_data = AdPosInfo(name=adpos)
    session.add(new_data)
    session.commit()

    return new_data
