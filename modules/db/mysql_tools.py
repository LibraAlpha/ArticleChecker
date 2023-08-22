from configs import db
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    f'mysql+pymysql://{db.MYSQL_USER}:{db.MYSQL_PASSWORD}@{db.MYSQL_HOST}:{db.MYSQL_PORT}/{db.MYSQL_DATABASE}')

Session = sessionmaker(bind=engine)
