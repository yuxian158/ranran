import os

from telethon import events

from .. import ranran, my_chat_id,download_path


def b_to_gb(num):
    return "%.2f" % (num / 1073741824)


def disk_usage(path):
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return f"已使用{b_to_gb(used)}GB,剩余{b_to_gb(free)}GB,共{b_to_gb(total)}GB"


@ranran.on(events.NewMessage(from_users=my_chat_id, pattern='信息'))
async def information(event):
    await ranran.send_message(my_chat_id, disk_usage("/"))


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
