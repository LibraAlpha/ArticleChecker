from modules.db import mysql_tools
from modules.db import redis_tools
from modules.Asset import Asset


def load_assets(date, page_index, is_sensitive, is_checked):
    """
    从mysql中加载黑名单列表
    :return:
    """
    page_offset = (page_index - 1) * page_limit

    ret = list()



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
