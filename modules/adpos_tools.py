import logging
from modules.db.mysql_tools import get_mysql_connection
from configs import action_code


def add(adpos):
    conn = get_mysql_connection()
    query = f"""
        insert into adpos (name)
        values ({adpos})
        on duplicate key update name =values({adpos})
    """

    # 创建游标对象
    cursor = conn.cursor()

    ret = action_code.WORD_ACTION_DEFAULT

    try:
        cursor.execute(query)
        # 提交事务
        conn.commit()
        # 校验插入/更新是否成功
        if cursor.rowcount > 0:
            ret = action_code.ADPOS_INSERT_SUCCESS
        else:
            ret = "插入/更新失败"
    except Exception as e:
        ret = f"错误：{e}"
    finally:
        cursor.close()
        conn.close()
        return ret


def find(adpos):
    ret = set()
    conn = get_mysql_connection()
    query = f"""
        select name from adpos
        where
        name like '%{adpos}%'
    """

    cursor = conn.cursor()
    try:
        cursor.execute(query)

        results = cursor.fetchall()

        for row in results:
            word = row[1]
            ret.add(word)
    except Exception as e:
        logging.warn(e)

    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()

    return ret


def remove(word):
    conn = get_mysql_connection()
    query = f"""
        delete from adpos
        where adpos = {word}
    """

    # 创建游标对象
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        # 提交事务
        conn.commit()
        # 校验插入/更新是否成功
        if cursor.rowcount > 0:
            ret = action_code.WORD_DEL_SUCCESS
        else:
            ret = "删除失败，广告位不存在"
    except Exception as e:
        ret = f"错误：{e}"

    finally:
        cursor.close()
        conn.close()

    return ret


def load(page_index, page_limit):
    page_offset = (page_index - 1) * page_limit

    ret = set()
    conn = get_mysql_connection()
    # 创建游标对象
    cursor = conn.cursor()

    # 执行查询语句
    query = f"""SELECT name 
        FROM adpos        
        limit {page_limit}
        offset {page_offset}
        """
    try:
        cursor.execute(query)

        # 获取查询结果
        results = cursor.fetchall()

        # 遍历结果
        for row in results:
            ret.add(row[0])
    except Exception as e:
        print("Error")
    finally:
        # 关闭游标
        cursor.close()
        conn.close()
    return ret


def load_all():
    ret = set()
    conn = get_mysql_connection()
    # 创建游标对象
    cursor = conn.cursor()

    # 执行查询语句
    query = """SELECT name 
    FROM adpos"""
    try:
        cursor.execute(query)

        # 获取查询结果
        results = cursor.fetchall()

        # 遍历结果
        for row in results:
            ret.add(row[0])
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
            FROM adpos      
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
