
from aiogram import Bot, Dispatcher, Router, types , F
from aiogram.filters import CommandStart , Command

import logging
from ..utils.ConfigLoader import LoadUserConfigById
from ..utils.Singleton import thread_safe_singleton
dp = Dispatcher()

async def on_startup():
    print("WAKE UP")


@thread_safe_singleton
class BotSubsystem(): 

    def __init__(self, config:dict =  {}):
        
        self.config = config

    def create_bot(self): 
        
        API_TOKEN = self.config['credentials']['BOT_TOKEN']
        bot = Bot(token=API_TOKEN)
        return bot

async def start_bot(config):
 

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    bot_object = BotSubsystem(config)
    bot = bot_object.create_bot()
    await dp.start_polling(bot)

@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(text= "Hi")

@dp.message()
async def profil(message: types.Message):

    user_id =  message.from_user.id 
    bot = BotSubsystem()

    user_cfg = LoadUserConfigById(bot.config, user_id)
    await message.answer(  str( user_cfg )   )