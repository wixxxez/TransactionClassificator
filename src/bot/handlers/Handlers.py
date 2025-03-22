from aiogram import Bot, Dispatcher, Router, types , F
from aiogram.filters import CommandStart , Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from src.bot.bot import dp, BotSubsystem
from src.utils.ConfigLoader import LoadUserConfigById
from src.utils.DataAquisitionJob import DataAcquisitionPipeline
from src.datatools.TransactionReport import OverallTransactionReport,Dataset
from src.datatools.CreateHTMLReport import BuildHTMLReport

@dp.message(Command('start'))
async def start(message: types.Message):

    keyboard = ReplyKeyboardBuilder()
    keyboard.row(KeyboardButton(text ="Load Data."))
    keyboard.row(KeyboardButton(text ="Get report",web_app=WebAppInfo(url="https://ffa9b44553bddba75b9868f84c4f7b90d7b71fbb4a095d69adb1e0e-apidata.googleusercontent.com/download/storage/v1/b/home_bot_web_serivce/o/index.html?jk=AVyuY3iO5rZT7PpZemwY7yC5Zl2zD1Uk4wwJVFQ2vuTNNApK-3F0fZZc6WAdI4senynpBxUbiDE1ZTOwxVz37BAuzZ5JBUdPL0Jl1_AeFf1XGB__C_vFBJ6eIvycbV6HKGr0OuON0n2Exx6tDrYS6n3NaJX5CvD8bY33fhKcPzOKgXbG5Q_9yO3T_k1pVYNWs_uGHmRgrmL5R02rZDNpS8yTGI7M2LjyCVL0aeZvtSes6b1EWc6OfkbBwDU3Gv6P08MXWs5_nUf28m1wRhPaz4oYiU_vitx5ikp0k2wt9bJVw5cuU5HKxHfqsrvqrjQq11bOF19UW2qUtCH14AEZOD-Kb30yr3bf1oxcTqpLmmVXrus8_e2Zt19JGLsngxjYPgOn-iGa7GzIJpOV5nLyon6OIU6Q3R22wGa2H1XTkbV7UfUuR-I4Gz2KXV0MmTZvHxR-HSGPekY4VsGsFUzWCm2XEkBia0_c4Be8pM9dLKze7Ky_wsgdZafqaRyw6MbFJKy0fnXmEL_66I3RbP_9fmCRnQyvxDZcGd5uHiXu3TaFCCZ3qEfgtcMHOkl6keYn1P5Ie5avjq4iOOCE8msXNeeIcqJx3vsJeHNCn6d7x0zcz4at94k01iYtiq1AY5_r9nY7hvCl8pdl98CA33kSJr4CcGXWjyNJc0Xm6XPxPA4uQGZnlyEcjdpdJGNhU8BaXFn_1P3bYz1Xqen5dCDqyZQXL7kAYwvwkxWTgtJNNmD0KiTRtecy2nhdH-Z3Pfeo0dLrmXSvTQuV1bsu1qi1PzfNkBT2iFMioWXZMzgAjSSzDXz-v4qUU1RbExUMXNQ9J--TYYSmHXznoLxDcbai0zSTdo4UFBO1fybbFuFE3oiRX86Gq3woFZVRQyAD6gzG62-0xfjefk_Xrww9csbXEBjZ0zUrqA7cKC4o2KJ7yao1jSKd4k327Eb0pFSN3rf9-ayaHHp7Ej-DBzfMUbYSqwqvryZLpmp83-38pATya2Y_SNIqFYo9Gp9vqBYXwoDEVQXGaPtgHK_pxHN_WZLsLLvRVZNQ_za_Tl5l8hxEvji0nC6zA8zCKEvIc8YEUXZsQ3WgoZQTDJdkjT7U9ecNUzQ_pA_uyvVJQPCkNblpu96OPsVUVSAdzqrBCnUW7Q23bnfzw5fPQnQ4KFX34qN6zTJWqs4&isca=1")))
    keyboard.row(KeyboardButton(text ="Generate report"))
     
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
     

@dp.message(F.text == "Generate report")
async def instruction(message: types.Message):
    user_id =  message.from_user.id 
    bot = BotSubsystem()

    HTMLBuilder = BuildHTMLReport(bot.config)

    HTMLBuilder.build_report()
     
    await message.answer(f"Report updated!")
     