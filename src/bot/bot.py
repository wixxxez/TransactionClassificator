
from aiogram import Bot, Dispatcher, Router, types , F
from aiogram.filters import CommandStart , Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.enums.parse_mode import ParseMode
 
import logging
from ..utils.ConfigLoader import LoadUserConfigById
from ..utils.Singleton import thread_safe_singleton
from ..utils.DataAquisitionJob import DataAcquisitionPipeline
from .security.WhiteListMiddleware import WhiteListMiddleware
from ..datatools.TransactionReport import OverallTransactionReport,Dataset


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
    dp.message.middleware(WhiteListMiddleware(config))

    bot_object = BotSubsystem(config)
    bot = bot_object.create_bot()
    await dp.start_polling(bot)

@dp.message(Command('start'))
async def start(message: types.Message):

    keyboard = ReplyKeyboardBuilder()
    keyboard.row(KeyboardButton(text ="Load Data."))
    keyboard.row(KeyboardButton(text ="Get report"))
    keyboard.row(KeyboardButton(text ="Get weekly balance report"))
    keyboard.row(KeyboardButton(text ="Get monthly balance report"))
    user_id =  message.from_user.id 
    
    bot = BotSubsystem()

    user_cfg = LoadUserConfigById(bot.config, user_id)
    await message.answer(text= f"Welcome {user_cfg['name']}. Choose an option!", reply_markup= keyboard.as_markup(one_time_keyboard = False, resize_keyboard = True))

@dp.message(F.text == "Load Data.")
async def instruction(message: types.Message):
    user_id =  message.from_user.id 
    bot = BotSubsystem()
    for user_cfg in bot.config['users']: 
        pipeline = DataAcquisitionPipeline(**user_cfg)
        pipeline.run()
        await message.answer(f"Loading data for user: {user_cfg['name']} ")
    await message.answer(  "Data is saved"   )
     

@dp.message(F.text == "Get report")
async def instruction(message: types.Message):
    user_id =  message.from_user.id 
    bot = BotSubsystem()

     
    
    dataset = Dataset(bot.config)
    transaction_data = dataset.create_dataset()
    report = OverallTransactionReport(transaction_data, dataset.get_balances())
    response = report.get_markdown_response()
    markdown = response.replace('-', '\\-').replace('.', '\\.').replace('|', '\\|')

    await message.answer(f"```\n{markdown}\n```", parse_mode=ParseMode.MARKDOWN_V2)
     

@dp.message(F.text == "Get weekly balance report")
async def instruction(message: types.Message):
    user_id =  message.from_user.id 
    bot = BotSubsystem()

     
    
    dataset = Dataset(bot.config)
    transaction_data = dataset.create_dataset()
    report = OverallTransactionReport(transaction_data, dataset.get_balances())
    response, text = report.get_Weekly_balance_report()
    markdown = response.replace('-', '\\-').replace('.', '\\.').replace('|', '\\|')

    await message.answer(f"```\n{markdown}\n```", parse_mode=ParseMode.MARKDOWN_V2)
    for i in text: 

        await message.answer(i)



@dp.message(F.text == "Get monthly balance report")
async def instruction(message: types.Message):
    user_id =  message.from_user.id 
    bot = BotSubsystem()

     
    
    dataset = Dataset(bot.config)
    transaction_data = dataset.create_dataset()
    report = OverallTransactionReport(transaction_data, dataset.get_balances())
    response, text = report.get_month_balance_report()
    markdown = response.replace('-', '\\-').replace('.', '\\.').replace('|', '\\|')

    await message.answer(f"```\n{markdown}\n```", parse_mode=ParseMode.MARKDOWN_V2)
    for i in text: 

        await message.answer(i)

@dp.message()
async def echo(message: types.Message):

    user_id =  message.from_user.id 
    bot = BotSubsystem()

    user_cfg = LoadUserConfigById(bot.config, user_id)
    await message.answer(  str( user_cfg )   )