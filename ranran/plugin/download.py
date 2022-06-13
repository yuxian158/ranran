"""
向然然发送视频来下载到指定位置
"""
import json
import os

import requests
from telethon import events,Button
import time
from .. import ranran, my_chat_id, config_enum, logger
from telethon.tl.types import MessageMediaWebPage

download_config = config_enum("download")
download_path = download_config.get("download_path")
host = download_config.get("host")
download_host = download_config.get("download_host")
upload_host = download_config.get("upload_host")
zip_password = download_config.get("zip_password")

def s(event):
    return True if event.media is not None else False

def press_event(user_id):
    return events.CallbackQuery(func=lambda e: e.sender_id == user_id)

@ranran.on(events.NewMessage(from_users=my_chat_id, func=s))
async def handler(event):
    message = event.message
    await ranran.send_message(my_chat_id, "检测到视频开始下载")
    timess = time.strftime("d%H%M%S", time.localtime())
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
    os.system(f"cd {download_path} && mv {file_name} {timess}.mp4")
    os.system(f"cd {download_path} && zip --password {zip_password} {timess}.zip  {timess}.mp4")
    os.system(f"cd {download_path} && rm -rf {timess}.mp4")
    await ranran.send_message(my_chat_id, f'{download_host}{timess}.zip')




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
    sender = event.sender_id
    async with ranran.conversation(my_chat_id) as conv:
        msg = await conv.send_message('正在查询，请稍后')
        res = requests.get(f"{upload_host}list").json()
        my_btns = []
        for e in res:
            my_btns.append(Button.inline(e.split('.')[0], data=e))
        my_btns.append(Button.inline('取消', data='cancel'))
        # my_btns = [Button.inline('上一页', data='up'), Button.inline(
        #     '下一页', data='next'), Button.inline('上级', data='updir'), Button.inline('取消', data='cancel')]
        msg = await ranran.edit_message(msg, '请做出您的选择：', buttons=my_btns)
        convdata = await conv.wait_event(press_event(sender))
        res = bytes.decode(convdata.data)
        logger.info(f"{res}")
        if res == 'cancel':
            msg = await ranran.edit_message(msg, '对话已取消')
            conv.cancel()
        else:
            data = {
                "path": res
            }
            if requests.post("{upload_host}upload", data=json.dumps(data)).status_code == 200:
                msg = await ranran.edit_message(msg, '上报成功')
                conv.cancel()
            else:
                msg = await ranran.edit_message(msg, '上报失败')
                conv.cancel()
        