import configs.db as db_config
import mysql.connector


def get_mysql_connection(host=db_config.MYSQL_HOST,
                         user=db_config.MYSQL_USER,
                         passwd=db_config.MYSQL_PASSWORD,
                         database=db_config.MYSQL_DATABASE
                         ):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=passwd,
        database=database
    )
    return conn
