import sys

sys.path.insert(0, "/home/latand/vkbot")
import asyncio

from myexamples import config
from avkapi import VK
from avkapi import types
from avkapi.types.user import UserFields
from avkapi.dispatcher import Dispatcher
import logging

loop = asyncio.get_event_loop()
vk = VK(confirmation_code=config.VK_CONFIRMATION_CODE,
        secret_key=config.VK_CALLBACK_SECRET_KEY,
        access_token=config.VK_ACCESS_TOKEN,
        loop=loop)
dp = Dispatcher(vk, loop=loop)

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


#
# @dp.message_handler(commands=["start"])
# async def echo_handler(message: types.Message):
#     peer_id = message.peer_id
#     text = message.text
#     print("COMMAND START")
#     # await vk.messages.send(message=text, peer_id=peer_id)


@dp.message_handler(content_types=types.MessageType.MESSAGE_NEW)
async def echo_handler(message: types.Message):
    peer_id = message.peer_id
    text = message.text
    u = await vk.users.get([peer_id], [UserFields.DOMAIN, UserFields.CONNECTIONS,
                                       UserFields.FIRST_NAME])
    print(u)
    # await vk.messages.send(message=text, peer_id=peer_id)


async def shutdown(_):
    await vk.close()
    await asyncio.sleep(0.250)


if __name__ == '__main__':
    from avkapi.utils.executor import start_webhook

    start_webhook(dispatcher=dp, webhook_path=config.WEBHOOK_PATH,
                  host=config.WEBAPP_HOST, port=config.WEBAPP_PORT,
                  on_shutdown=shutdown)
