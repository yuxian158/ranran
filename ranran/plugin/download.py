"""
向然然发送视频来下载到指定位置
"""
import json
import os

import requests
from telethon import events
import time
from .. import ranran, my_chat_id, config_enum, logger
from telethon.tl.types import MessageMediaWebPage

download_config = config_enum("download")
download_path = download_config.get("download_path")
host = download_config.get("host")
download_host = download_config.get("download_host")
upload_host = download_config.get("upload_host")


def s(event):
    return True if event.media is not None else False


@ranran.on(events.NewMessage(from_users=my_chat_id, func=s))
async def handler(event):
    message = event.message
    await ranran.send_message(my_chat_id, "检测到视频开始下载")
    timess = time.strftime("%m%d%H%M%S", time.localtime())
    file_name = ''
    if type(message.media) == MessageMediaWebPage:
        return
    if message.media.document.mime_type == "image/webp":
        file_name = f'{message.media.document.id}.webp'
    if message.media.document.mime_type == "application/x-tgsticker":
        file_name = f'{message.media.document.id}.tgs'
    for i in message.document.attributes:
        try:
            file_name = i.file_name
        except:
            continue
    if file_name == '':
        file_name = timess
    file_path_name = download_path + file_name
    start = time.time()
    await ranran.download_media(event.media, file_path_name)
    end_time = time.time()
    # await conv.send_message(f'下载完成文件名{filename}')
    # await ranran.send_message(my_chat_id, f'下载完成路径为{host}{file_name}.mp4')
    logger.info(f"下载{file_name}完成")
    await ranran.send_message(my_chat_id, f'用时{round(end_time - start)}s')
    os.system(f"cd {download_path} && zip --password zl159753123 {file_name}.zip  {file_name}")
    await ranran.send_message(my_chat_id, f'下载完成路径为{host}{file_name}')
    await ranran.send_message(my_chat_id, f'压缩包路径为{download_host}{file_name}')




@ranran.on(events.NewMessage(from_users=my_chat_id, pattern='删除'))
async def delete(event):
    user_id = event.sender_id
    async with ranran.conversation(user_id) as conv:
        await conv.send_message('确定删除所有视频吗？')
        response = await conv.get_response()
        if response.text == "是":
            os.system(f"rm -rf {download_path}*")
            await conv.send_message('成功')
        else:
            await conv.send_message('退出')


@ranran.on(events.NewMessage(from_users=my_chat_id, pattern='上传'))
async def upload(event):
    txt = event.raw_text
    list = txt.split(' ', 2)
    url_data = list[1]
    await ranran.send_message(my_chat_id, f'上报链接{url_data}')
    data = {
        "name": "a.zip",
        "url": url_data
    }
    if requests.post(url=upload_host, data=json.dumps(data)).text == 200:
        await ranran.send_message(my_chat_id,"上报成功")
    else:
        await ranran.send_message(my_chat_id, "失败")