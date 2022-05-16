from telethon import events

from .. import ranran_ql, logger, ranran, my_chat_id


@ranran.on(events.NewMessage(from_users=my_chat_id, pattern=r'ql.*'))
async def add_env(event):
    txt = event.raw_text
    list = txt.split(' ',2)
    ranran_ql.add_env(new_env=list[1],value=list[2])
    await ranran.send_message(my_chat_id,f"添加变量{list[1]},{list[2]}")
    logger.info(f"添加变量{list[1]},{list[2]}")