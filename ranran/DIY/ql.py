from telethon import events

from .. import ranran_ql, logger, ranran, my_chat_id


@ranran.on(events.NewMessage(from_users=my_chat_id, pattern=r'ql.*'))
async def add_env(event):
    txt = event.raw_text
    list = txt.split(' ',2)
    common = list[1]
    if common == "cat":
        env = list[2]
        for i,j in ranran_ql.get_env(env):
            await ranran.send_message(my_chat_id, f"id={i},value={j}")
        logger.info(f"查看变量{env}")
    elif common == "add":
        list = txt.split(' ',3)
        ranran_ql.add_env(new_env=list[1],value=list[2])
        await ranran.send_message(my_chat_id,f"添加变量{list[2]},{list[3]}")
        logger.info(f"添加变量{list[2]},{list[3]}")
    elif common=="del":
        id = list[2]
        ranran_ql.del_env(id)
        await ranran.send_message(my_chat_id, f"删除变量id={id}")
        logger.info(f"删除变量id={id}")
    else:
        await ranran.send_message(my_chat_id, f"未识别的命令")