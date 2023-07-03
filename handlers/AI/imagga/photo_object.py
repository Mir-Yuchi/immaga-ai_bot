import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ContentType, InputFile

from api_clients.imagga.tags import ImaggaTagsEndpoint
from commands import Commands
from keyboards.reply import START_COMMANDS_KEYBOARD
from loader import dp
from misc.states import GetPhotoObjectState
from misc.utils import (
    photo_today_file_path, http_link_validator, photo_format_validator,
    imagga_success_response
)


@dp.message_handler(text=Commands.get_obj.value)
async def get_photo_object_command(message: Message):
    await GetPhotoObjectState.send_photo.set()
    await message.answer(
        'Отправьте мне картинку либо ссылку на неё',
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message_handler(content_types=[ContentType.PHOTO], state=GetPhotoObjectState.send_photo)
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
    loader = ImaggaTagsEndpoint(
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
        object_dict = response["result"]["tags"][0]
        await message.bot.send_photo(
            message.from_user.id,
            InputFile(file_obj.name),
            caption=f'Успешно обработал!\n'
                    f'Объект на картинке похож на '
                    f'{object_dict["tag"][loader.lang]}\n'
                    f'Процент совпадение: {object_dict["confidence"]}%'
        )
    await state.finish()


@dp.message_handler(content_types=[ContentType.TEXT], state=GetPhotoObjectState.send_photo)
async def get_photo_object(message: Message, state: FSMContext):
    if not http_link_validator(message.text) or not photo_format_validator(message.text):
        await message.answer('Дурак-простак, введи прямую ссылку на файл')
        return
    loader = ImaggaTagsEndpoint(
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
        object_dict = response["result"]["tags"][0]
        await message.answer(
            f'Успешно обработал!\n'
            f'Объект на картинке похож на '
            f'{object_dict["tag"][loader.lang]}\n'
            f'Процент совпадение: {object_dict["confidence"]}%'
        )
    await state.finish()
