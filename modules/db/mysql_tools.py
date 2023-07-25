from configs import db
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_mysql_connection(host=db.MYSQL_HOST,
                         user=db.MYSQL_USER,
                         passwd=db.MYSQL_PASSWORD,
                         database=db.MYSQL_DATABASE
                         ):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=passwd,
        database=database
    )
    return conn


engine = create_engine(
    f'mysql+pymysql://{db.MYSQL_USER}:{db.MYSQL_PASSWORD}@{db.MYSQL_HOST}:{db.MYSQL_PORT}/{db.MYSQL_DATABASE}')

Session = sessionmaker(bind=engine)
