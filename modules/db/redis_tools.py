import redis
import configs.redis as redis_config

redis_client = redis.StrictRedis(host=redis_config.HOST,
                                 port=redis_config.PORT,
                                 db=redis_config.IMG_URL_DB,
                                 )


def append(original_name, replace_url):
    name = 'img_replace_queue'
    original_queue_length = redis_client.llen(name)
    redis_client.lpush(name, f"{original_name}:{replace_url}")
    updated_queue_length = redis_client.llen(name)

    added_data_count = updated_queue_length - original_queue_length
    if added_data_count > 0:
        ret = 1
    else:
        ret = 0
    return ret

