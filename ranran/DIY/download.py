import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import time
import os
# from .. import ranran, my_chat_id

path = "/aaa/files/video/"


# @ranran.on(events.NewMessage(from_users=my_chat_id)
# async def handler(event):
#     user_id = event.sender_id
#     async with client.conversation(user_id) as conv:
#         if event.raw_text == "删除":
#             await conv.send_message('确定删除所有视频吗？')
#             response = await conv.get_response()
#             if response.text == "是":
#                 os.system("rm -rf /aaa/files/video/*")
#                 await conv.send_message('成功')
#             else:
#                 await conv.send_message('退出')
#         if event.media is not None:
#             await conv.send_message('检测到视频开始下载')
#             # paths = await event.download_media()
#             timess = time.strftime("%m%d%H%M%S", time.localtime())
#             filename = path + timess
#             start = time.time()
#             await client.download_media(event.media, filename)
#             end_time = time.time()
#             # await conv.send_message(f'下载完成文件名{filename}')
#             await conv.send_message(f'下载完成路径为http://alist.yuxian158.work/local/{timess}.mp4')
#             await conv.send_message(f'用时{round(end_time - start)}s')
#         print(event.raw_text)
