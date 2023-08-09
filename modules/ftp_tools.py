import hashlib
import os.path
from ftplib import FTP
from datetime import datetime


def upload(original_file_name: str, local_file_path: str):
    """
    通过ftp上传文件到cdn服务器，返回图片的cdn地址
    :param original_file_name: 原始图片地址，仅用于进行映射使用
    :param local_file_path: 待上传的文件在服务器上的地址
    :return: 拼接后的cdn地址
    """
    ftp_host = '1307.kejet.net'
    ftp_user = 'www'
    ftp_pass = '6p2KWH7aT=nfa-T'

    ftp = FTP(ftp_host)
    ftp.login(ftp_user, ftp_pass)

    dt = datetime.now().date().strftime("%Y%m%d")

    folder_path = f'{dt}'

    if folder_path not in ftp.nlst():
        ftp.mkd(folder_path)

    ftp.cwd(folder_path)

    save_path = f"{hashlib.md5(original_file_name.encode('utf-8')).hexdigest()}.jpg"

    with open(local_file_path, 'rb') as local_file:
        ftp.storbinary(f'STOR {save_path}', local_file)

    remote_file_size = ftp.size(save_path)

    # 比较本地和远程文件的大小和哈希值
    if remote_file_size == os.path.getsize(local_file_path):
        ftp.quit()
        ret_file = f'https://m.kejet.net/ms/i/{folder_path}/{save_path}'
        return ret_file
    else:
        return -1

