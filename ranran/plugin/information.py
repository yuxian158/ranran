import os

from telethon import events

from .. import ranran, my_chat_id


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



