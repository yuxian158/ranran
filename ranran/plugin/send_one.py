"""
每6小时发送一条一言
"""
import asyncio

import aiocron
import aiohttp

from .. import ranran,my_chat_id,logger


@aiocron.crontab('* */6 * * *')
async def one():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://v1.hitokoto.cn") as response:
            js = await response.json()
            xt= js.get("hitokoto") + "  --" + js.get("from")
            await ranran.send_message(my_chat_id,xt)
        logger.info(f"向{my_chat_id}发送{xt}")