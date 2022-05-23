"""
向然然发送视频来下载到指定位置
"""
from telethon import events
import time
from .. import ranran, my_chat_id, config_enum, logger

download_config = config_enum("download")
download_path = download_config.get("download_path")
host = download_config.get("host")


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
