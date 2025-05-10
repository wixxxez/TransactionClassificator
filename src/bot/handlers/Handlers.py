from aiogram import Bot, Dispatcher, Router, types , F
from aiogram.filters import CommandStart , Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from src.bot.bot import dp, BotSubsystem
from src.utils.ConfigLoader import LoadUserConfigById
from src.utils.DataAquisitionJob import DataAcquisitionPipeline, save_data
from src.datatools.TransactionReport import OverallTransactionReport,Dataset
from src.datatools.CreateHTMLReport import BuildHTMLReport
from src.utils.GCSFileManager import generate_signed_url

import pandas as pd

@dp.message(Command('start'))
async def start(message: types.Message):

    keyboard = ReplyKeyboardBuilder()
    keyboard.row(KeyboardButton(text ="Load Data."))
    keyboard.row(KeyboardButton(text ="Get report",web_app=WebAppInfo(url=generate_signed_url('home_bot_web_serivce','index.html'))))
    keyboard.row(KeyboardButton(text ="Generate report"))
     
    user_id =  message.from_user.id 
    
    bot = BotSubsystem()

    user_cfg = LoadUserConfigById(bot.config, user_id)
    await message.answer(text= f"Welcome {user_cfg['name']}. Choose an option!", reply_markup= keyboard.as_markup(one_time_keyboard = False, resize_keyboard = True))

@dp.message(F.text == "Load Data.")
async def instruction(message: types.Message):
    await message.answer("Processing...")
    user_id =  message.from_user.id 
    bot = BotSubsystem()
    loaded_history = []
    for user_cfg in bot.config['users']:
        await message.answer(f"Loading data for user: {user_cfg['name']} ") 
        pipeline = DataAcquisitionPipeline(**user_cfg)
        data = pipeline.run()
        loaded_history.append(data)

    save_data(pd.concat(loaded_history),bot.config['data_info']['transaction_path'])    
    await message.answer(  "Data is saved"   )
     

@dp.message(F.text == "Generate report")
async def instruction(message: types.Message):
    await message.answer("Processing...")
    user_id =  message.from_user.id 
    bot = BotSubsystem()

    HTMLBuilder = BuildHTMLReport(bot.config)

    HTMLBuilder.build_report()
     
    await message.answer(f"Report updated!")
     