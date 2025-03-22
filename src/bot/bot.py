
from aiogram import Bot, Dispatcher, Router, types , F
from aiogram.filters import CommandStart , Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

import logging
from ..utils.ConfigLoader import LoadUserConfigById
from ..utils.Singleton import thread_safe_singleton
from ..utils.DataAquisitionJob import DataAcquisitionPipeline
from .security.WhiteListMiddleware import WhiteListMiddleware
from ..datatools.TransactionReport import OverallTransactionReport,Dataset
from ..datatools.CreateHTMLReport import BuildHTMLReport

dp = Router()
 

async def on_startup():
    bot_subsystem = BotSubsystem()
    bot = bot_subsystem.create_bot()
    webhook_info = await bot.get_webhook_info()
     

    if webhook_info.url != bot_subsystem.WEBHOOK_URL:
        await bot.set_webhook(
            url=bot_subsystem.WEBHOOK_URL
        )


@thread_safe_singleton
class BotSubsystem(): 

    def __init__(self, config:dict =  {}):
        
        self.config = config

    def create_bot(self): 
        
        API_TOKEN = self.config['credentials']['BOT_TOKEN']
        bot = Bot(token=API_TOKEN)
        return bot

def start_bot(config):
 
    from src.bot.handlers.Handlers import dp
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    dispatcher = Dispatcher()

    dispatcher.include_router(dp)
    dispatcher.startup.register(on_startup)
    dp.message.middleware(WhiteListMiddleware(config))

    app = web.Application()
    bot_object = BotSubsystem(config)
    bot = bot_object.create_bot()
    
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
    )
    WEBHOOK_PATH = f"/bot/{config['credentials']['BOT_TOKEN']}"
    WEBHOOK_URL = f"{config['credentials']['TUNNEL_URL']}{WEBHOOK_PATH}"

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
 
    bot_object.WEBHOOK_URL = WEBHOOK_URL

    setup_application(app, dispatcher, bot=bot)

    # And finally start webserver
    web.run_app(app, host= "0.0.0.0", port=8080)


