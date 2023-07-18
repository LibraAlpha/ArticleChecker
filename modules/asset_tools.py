from modules.db import mysql_tools
from modules.db import redis_tools
from modules.asset import Asset


def load_assets(date, page_index, is_sensitive, is_checked):
    """
    从mysql中加载黑名单列表
    :return:
    """
    page_offset = (page_index - 1) * page_limit

    ret = list()
    conn = get_mysql_connection()
    # 创建游标对象
    cursor = conn.cursor()

    # 执行查询语句
    query = f"""SELECT * 
            FROM assets
            where is_sensitive = {is_sensitive}
            and is_checked = {is_checked}            
            limit {page_limit}
            offset {page_offset}
            """
    try:
        cursor.execute(query)

        # 获取查询结果
        results = cursor.fetchall()

        # 遍历结果
        for row in results:
            url = row[0]
            title = row[1]
            desc = row[2]
            adv = row[3]
            is_checked = row[4]
            updated = row[5]
            is_sensitive = row[6]
            ad_pos = row[7]
            sensitive_words = row[8]
            asset = Asset(url, title, desc, adv, is_checked=is_checked)
            asset.sens_words = sensitive_words
            asset.adpos = ad_pos
            asset.is_sensitive = is_sensitive
            ret.add(asset)
    except Exception as e:
        print()
    finally:
        # 关闭游标
        cursor.close()
        conn.close()
    return ret


def get_size():
    conn = get_mysql_connection()
    # 创建游标对象
    cursor = conn.cursor()

    # 执行查询语句
    query = f"""SELECT count(*)  
            FROM assets      
            """
    try:
        cursor.execute(query)

        # 获取查询结果
        total_count = cursor.fetchone()[0]

    except Exception as e:
        return {'error': str(e)}
    finally:
        # 关闭游标
        cursor.close()
        conn.close()
    return {'total_count': total_count}
