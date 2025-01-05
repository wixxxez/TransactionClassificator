
from aiogram import Bot, Dispatcher, Router, types , F
from aiogram.filters import CommandStart , Command

import logging
 

dp = Dispatcher()

async def on_startup():
    print("WAKE UP")

async def start_bot(config):
 

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    API_TOKEN = config['credentials']['BOT_TOKEN']
    bot = Bot(token=API_TOKEN)
    # Initialize bot and dispatcher
     

    await dp.start_polling(bot)

@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(text= "Hi")

@dp.message()
async def profil(message: types.Message):

    await message.answer(message.text)