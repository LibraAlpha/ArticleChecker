import base64
import os.path
import time

import cv2
import urllib.request

import pandas as pd

from modules.secret import get_md5_hash


def download_video(video_url, output_path):
    urllib.request.urlretrieve(video_url, output_path)
    print(f"Video downloaded successfully as {output_path}")


def extract_frame(video_path, frame_number, output_path):
    # 打开视频文件
    video = cv2.VideoCapture(video_path)

    # 确定视频的帧数
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # 设置要提取的帧数
    frame_to_extract = frame_number

    # 确保要提取的帧数不超过视频的帧数范围
    if frame_to_extract < 0 or frame_to_extract >= total_frames:
        print("Invalid frame number.")
        return

    # 设置当前帧数
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_to_extract)

    # 读取当前帧
    ret, frame = video.read()

    # 检查是否成功读取帧
    if not ret:
        print("Failed to read frame.")
        return

    # 保存帧为图像文件
    cv2.imwrite(output_path, frame)

    # 释放视频文件对象
    video.release()

    print("Frame extracted successfully.")


def get_slice(byte_string):
    string = byte_string.decode('utf-8')
    return string

def tmp(file):
    df = pd.read_csv(file, sep=',')
    df = df.loc[df.cnt > 10000]

    df_video_urls = df.video.dropna().values.tolist()
    return_list = []

    for content in df_video_urls:
        if '|' in str(content):
            urls = content.split('|')
            for url in urls:
                info = url.split('-')
                adv, link = info[0], info[1]
                img_link = get_slice(base64.b64decode(link))
                if adv == '41':
                    return_list.append(img_link)
        else:
            if '-' in content:
                info = content.split('-')
                adv, link = info[0], info[1]
                img_link = get_slice(base64.b64decode(link))
                if adv == '41':
                    return_list.append(img_link)

    return return_list


def run(date):
    file = f'D:/downloads/video{date}.csv'
    video_url_list = tmp(file)

    print(len(video_url_list))

    video_url_pair = list(tuple())
    size = len(video_url_list)
    index = 1

    for url in video_url_list:
        print(f'{index}: {size}')
        filename = get_md5_hash(url)
        video_path = os.path.join(f"D:/url_img/{date}/video/", f"{filename}")
        frame_number = 30  # 要提取的帧数
        output_path = f"D:/url_img/{date}/img/{index}.jpg"  # 保存提取的帧的路径
        download_video(url, video_path)
        extract_frame(video_path, frame_number, output_path)
        video_url_pair.append((url, f"{index}.jpg"))
        index += 1

    df = pd.DataFrame(video_url_pair, columns=['url', 'img'])
    df.to_excel(f'D:/url_img/{date}.xlsx')
    return


if __name__ == '__main__':
    run('0723')
