import logging
from modules.db.mysql_tools import get_mysql_connection
from configs import action_code


def add_sensitive_word(word):
    conn = get_mysql_connection()
    query = f"""
        insert into sensitive_words (sensitive_word)
        values ({word})
        on duplicate key update sensitive_word =values({word})
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
            ret = action_code.WORD_INSERT_SUCCESS
        else:
            ret = "插入/更新失败"
    except Exception as e:
        ret = f"错误：{e}"
    finally:
        cursor.close()
        conn.close()
        return ret


def find_sensitive_word(word):
    ret = set()
    conn = get_mysql_connection()
    query = f"""
        select * from sensitive_words
        where
        sensitive_word like '%{word}%'
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


def remove_word_from_sensitive_list(word):
    conn = get_mysql_connection()
    query = f"""
        delete from sensitive_words
        where sensitive_word = {word}
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
            ret = "删除失败，敏感词不存在"
    except Exception as e:
        ret = f"错误：{e}"

    finally:
        cursor.close()
        conn.close()

    return ret


def load_all():
    ret = set()
    conn = get_mysql_connection()
    # 创建游标对象
    cursor = conn.cursor()

    # 执行查询语句
    query = """SELECT sensitive_word 
    FROM sensitive_words"""
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