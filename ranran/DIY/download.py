from telethon import events
import time
from .. import ranran, my_chat_id,download_path,host,logger



def s(event):
    return True if event.media is not None else False


@ranran.on(events.NewMessage(from_users=my_chat_id, func=s))
async def handler(event):
    await ranran.send_message(my_chat_id, "检测到视频开始下载")
    timess = time.strftime("%m%d%H%M%S", time.localtime())
    filename = download_path + timess
    start = time.time()
    await ranran.download_media(event.media, filename)
    end_time = time.time()
    # await conv.send_message(f'下载完成文件名{filename}')
    await ranran.send_message(my_chat_id, f'下载完成路径为{host}{timess}.mp4')
    logger.info(f"下载{event.raw_text}完成")
    await ranran.send_message(my_chat_id, f'用时{round(end_time - start)}s')
