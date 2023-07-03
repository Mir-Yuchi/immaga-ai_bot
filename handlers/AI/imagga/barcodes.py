import datetime

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ContentType, InputFile

from api_clients.imagga.barcodes import ImaggaBarcodesEndpoint
from commands import Commands
from keyboards.reply import START_COMMANDS_KEYBOARD
from loader import dp
from misc.states import ScanQRState
from misc.utils import (
    photo_today_file_path, imagga_success_response, photo_format_validator,
    http_link_validator
)


@dp.message_handler(Text(equals=Commands.barcodes.value))
async def barcode_scan_command(message: Message):
    await ScanQRState.send_photo.set()
    await message.answer('Отлично! Отправьте картинку либо прямую ссылку на неё')


@dp.message_handler(content_types=[ContentType.PHOTO], state=ScanQRState.send_photo)
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
    loader = ImaggaBarcodesEndpoint(
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
    if not imagga_success_response(response) or not response["result"]["barcodes"]:
        await message.answer(f'Что-то пошло не так... Код ошибки: {response.status_code}')
    else:
        object_dict = response["result"]["barcodes"][0]
        await message.bot.send_photo(
            message.from_user.id,
            InputFile(file_obj.name),
            caption=f'Успешно обработал!\n'
                    f'Результат сканирования: '
                    f'{object_dict["data"]}\n'
        )
    await state.finish()


@dp.message_handler(content_types=[ContentType.TEXT], state=ScanQRState.send_photo)
async def get_photo_object(message: Message, state: FSMContext):
    if not http_link_validator(message.text) or not photo_format_validator(message.text):
        await message.answer('Дурак-простак, введи прямую ссылку на файл')
        return
    loader = ImaggaBarcodesEndpoint(
        message.bot['config']['imagga_api_key'],
        message.bot['config']['imagga_api_secret']
    )
    await message.answer(
        'Фото обрабатывается...',
        reply_markup=START_COMMANDS_KEYBOARD
    )
    response = loader.send_photo_bytes(message.text)
    if not imagga_success_response(response) or not response["result"]["barcodes"]:
        await message.answer(f'Что-то пошло не так... Попробуйте ещё раз')
    else:
        object_dict = response["result"]["barcodes"][0]
        await message.answer(
            f'Успешно обработал!\n'
            f'Результат сканирования: '
            f'{object_dict["data"]}'
        )
    await state.finish()
