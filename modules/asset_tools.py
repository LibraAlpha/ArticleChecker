from modules.db import mysql_tools
from modules.db import redis_tools


def load_assets(date):
    """
    从mysql中加载黑名单列表
    :return:
    """
    