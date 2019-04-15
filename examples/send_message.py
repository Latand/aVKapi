import asyncio
from avkapi import VK
from avkapi.types.keyboard import Colours, ListOfButtons

VK_CONFIRMATION_CODE = ""
VK_CALLBACK_SECRET_KEY = None
VK_ACCESS_TOKEN = "6dd495521793844f17510f6359445288fc6cc3dae00de6e1c6e8c173e7854322b3f989d58b20b8e1a3af8"

loop = asyncio.get_event_loop()
vk = VK(confirmation_code=VK_CONFIRMATION_CODE,
        secret_key=VK_CALLBACK_SECRET_KEY,
        access_token=VK_ACCESS_TOKEN,
        loop=loop)

keyboard = ListOfButtons(buttons=["Кнопка Белая", "Кнопка Синяя", "Кнопка Красная", "Кнопка Зеленая"],
                         colours=[Colours.WHITE, Colours.BLUE, Colours.RED, Colours.GREEN],
                         row_sizes=[1, 2, 1],
                         payloads=["white", "blue", "red", "green"]).keyboard

user_domain = ""
user_id = 123456


async def test_send_message():
    await vk.messages.send(message="Hello from aVKapi", domain=user_domain,
                           user_id=user_id,
                           keyboard=keyboard)


if __name__ == '__main__':
    loop.run_until_complete(test_send_message())
