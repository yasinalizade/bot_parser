from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiofiles import os
from async_main import collect_data
from dotenv import load_dotenv
from os import getenv

# create .env file and put your bot token in the file.
# DO NOT forget to check if '.env' in your .gitignore file!
load_dotenv()

bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Get special prices from Lidl.ie']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer(
        'Press button for sale prices ↓',
        reply_markup=keyboard
    )


@dp.message_handler(Text(equals='Get special prices from Lidl.ie'))
async def lidl_sales(message: types.Message):
    await message.answer('Please waiting...')
    chat_id = message.chat.id
    await send_data(chat_id=chat_id)


async def send_data(chat_id=''):
    file = await collect_data()
    await bot.send_document(chat_id=chat_id, document=open(file, 'rb'))
    await os.remove(file)


if __name__ == '__main__':
    executor.start_polling(dp)
