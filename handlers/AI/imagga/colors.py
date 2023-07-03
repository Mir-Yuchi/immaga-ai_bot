import datetime

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, ContentType, InputFile

from api_clients.imagga.colors import ImaggaColorsEndpoint
from commands import Commands
from keyboards.reply import START_COMMANDS_KEYBOARD
from loader import dp
from misc.states import ScanColorsState
from misc.utils import (
    photo_today_file_path, imagga_success_response,
    http_link_validator, photo_format_validator
)


@dp.message_handler(Text(Commands.colors.value))
async def get_color_palette_command(message: Message):
    await ScanColorsState.send_photo.set()
    await message.answer(
        'Отправьте мне картинку либо ссылку на неё',
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message_handler(content_types=[ContentType.PHOTO], state=ScanColorsState.send_photo)
async def get_photo_object(message: Message, state: FSMContext):
    file = await message.photo[0].get_file()
    date_obj = datetime.datetime.now()
    photo_file_path = photo_today_file_path(
        date_obj,
        file.values['file_path']
    )
    file_obj = await message.bot.download_file_by_id(
        file.file_id,
        photo_file_path
    )
    loader = ImaggaColorsEndpoint(
        message.bot['config']['imagga_api_key'],
        message.bot['config']['imagga_api_secret']
    )
    await message.answer(
        'Фото обрабатывается...',
        reply_markup=START_COMMANDS_KEYBOARD
    )
    with open(file_obj.name, 'rb') as file:
        content = file.read()
    response = loader.send_photo_bytes(content)
    if not imagga_success_response(response):
        await message.answer(f'Что-то пошло не так... Код ошибки: {response.status_code}')
    else:
        all_colors = response['result']['colors']
        bg_colors = '\n'.join(color['html_code'] for color in all_colors['background_colors'])
        fg_colors = '\n'.join(color['html_code'] for color in all_colors['foreground_colors'])
        await message.bot.send_photo(
            message.from_user.id,
            InputFile(file_obj.name),
            caption=f'Успешно обработал!\n'
                    f'Найденные цвета:\n'
                    f'Background:\n{bg_colors}\n'
                    f'Foreground:\n{fg_colors}'
        )
    await state.finish()


@dp.message_handler(content_types=[ContentType.TEXT], state=ScanColorsState.send_photo)
async def get_photo_object(message: Message, state: FSMContext):
    if not http_link_validator(message.text) or not photo_format_validator(message.text):
        await message.answer('Дурак-простак, введи прямую ссылку на файл')
        return
    loader = ImaggaColorsEndpoint(
        message.bot['config']['imagga_api_key'],
        message.bot['config']['imagga_api_secret']
    )
    await message.answer(
        'Фото обрабатывается...',
        reply_markup=START_COMMANDS_KEYBOARD
    )
    response = loader.send_photo_bytes(message.text)
    if not imagga_success_response(response):
        await message.answer(f'Что-то пошло не так... Код ошибки: {response.status_code}')
    else:
        all_colors = response['result']['colors']
        bg_colors = '\n'.join(color['html_code'] for color in all_colors['background_colors'])
        fg_colors = '\n'.join(color['html_code'] for color in all_colors['foreground_colors'])
        await message.answer(
            f'Успешно обработал!\n'
            f'Найденные цвета:\n\n'
            f'Background:\n{bg_colors}\n\n'
            f'Foreground:\n{fg_colors}'
        )
    await state.finish()
