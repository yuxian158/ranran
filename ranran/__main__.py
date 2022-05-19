from . import ranran, my_chat_id, logger


async def hello():
    await ranran.send_message(my_chat_id, "hello")


if __name__ == "__main__":
    logger.info("开始运行")
    with ranran:
        ranran.loop.create_task(hello())
        ranran.loop.run_forever()
