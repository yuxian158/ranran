import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import time
import os
from .. import ranran, my_chat_id

path = "/aaa/files/video/"

def s(event):
    return True if event.media is not None else False


@ranran.on(events.NewMessage(from_users=my_chat_id,func=s))
async def handler(event):
    await ranran.send_message(my_chat_id, "检测到视频开始下载")
    timess = time.strftime("%m%d%H%M%S", time.localtime())
    filename = path + timess
    start = time.time()
    await ranran.download_media(event.media, filename)
    end_time = time.time()
    # await conv.send_message(f'下载完成文件名{filename}')
    await ranran.send_message(my_chat_id,f'下载完成路径为http://alist.yuxian158.work/local/{timess}.mp4')
    await ranran.send_message(my_chat_id,f'用pip freeze > ./requirements.txt  时{round(end_time - start)}s')

