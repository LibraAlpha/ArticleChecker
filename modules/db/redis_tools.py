def get_redis_client():
    redis_client = redis.Redis(host=redis_config.REDIS_HOST, port=redis_config.REDIS_PORT)
    return redis_client


# 存储广告主、素材链接、标题和描述的信息
# TODO: key分片，分实例
def store_asset(redis_client, url_base64, title, desc, is_blocked, is_checked=False, expire_duration=86400 * 7):
    # 构建存储的键名
    if is_blocked:
        key = "blocked"
    elif is_checked:
        key = "checked"
    else:
        key = "uncensored"

    url_info = {
        "title": title,
        "desc": desc
    }

    redis_client.sadd(key, url_base64, json.dumps(url_info), expire=expire_duration)
    return


# 读取广告主、素材链接、标题和描述的信息
def read_asset(redis_client, url_base64, is_blocked, is_checked=False):
    # 构建读取的键名
    if is_blocked:
        key = "blocked"
    elif is_checked:
        key = "checked"
    else:
        key = "uncensored"

    info = redis_client.hget(key, url_base64)

    # 解码为字符串并处理为字典格式
    asset_info = json.loads(info.decode())

    # 返回广告主信息
    return asset_info
