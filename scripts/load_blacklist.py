import configs.db as db_config
import configs.basics as basic_config
import mysql.connector
from modules.tools import read_large_file


def load():
    sensitive_words_set = set()
    for line in read_large_file(basic_config.get_root_path() + "/res/blacklist.txt"):
        sensitive_word = line.strip()
        sensitive_words_set.add(sensitive_word)

    # 创建连接
    conn = mysql.connector.connect(
        host=db_config.MYSQL_HOST,
        user=db_config.MYSQL_USER,
        password=db_config.MYSQL_PASSWORD,
        database=db_config.MYSQL_DATABASE
    )

    # 创建游标对象
    cursor = conn.cursor()

    try:
        # 执行批量插入语句
        query = "INSERT INTO sensitive_words (sensitive_word) VALUES (%s)"
        values = [(word,) for word in sensitive_words_set]

        # 分批次插入数据
        batch_size = 100
        total_batches = len(values) // batch_size
        for batch in range(total_batches + 1):
            start_index = batch * batch_size
            end_index = (batch + 1) * batch_size
            batch_values = values[start_index:end_index]
            cursor.executemany(query, batch_values)
            conn.commit()

        print("插入成功")

    except Exception as e:
        print("发生错误:", e)

    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()


if __name__ == '__main__':
    load()
