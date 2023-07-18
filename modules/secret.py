import base64
import hashlib


def get_md5_hash(text):
    # 创建 MD5 对象
    md5 = hashlib.md5()
    # 更新哈希对象
    md5.update(text.encode('utf-8'))
    # 获取加密后的结果
    hashed_text = md5.hexdigest()
    return hashed_text


def get_base64_decode(base64str):
    return base64.b64decode(base64str)
