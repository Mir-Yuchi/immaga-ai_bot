from aiogram.types import Message

from keyboards.reply import START_COMMANDS_KEYBOARD
from loader import dp


@dp.message_handler(commands=['start'], commands_prefix='/!')
async def start(message: Message):
    await message.reply(
        'Привет! Я Imagga бот!',
        reply_markup=START_COMMANDS_KEYBOARD
    )
