import datetime

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, ContentType

from api_clients.imagga.face_similarity import ImaggaFaceSimilarityEndpoint
from api_clients.imagga.faces import ImaggaFaceDetectionsEndpoint
from commands import Commands
from keyboards.reply import START_COMMANDS_KEYBOARD
from loader import dp
from misc.states import FaceSimilarityState
from misc.utils import photo_today_file_path, imagga_success_response, http_link_validator, photo_format_validator


@dp.message_handler(Text(Commands.face_similarity.value))
async def face_similarity_command(message: Message):
    await message.answer(
        'Отправьте мне картинку либо ссылку на неё',
        reply_markup=ReplyKeyboardRemove()
    )
    await FaceSimilarityState.send_photo_1.set()


@dp.message_handler(content_types=[ContentType.PHOTO], state=[FaceSimilarityState.send_photo_1,
                                                              FaceSimilarityState.send_photo_2])
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
    loader = ImaggaFaceDetectionsEndpoint(
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
        await state.finish()
        await message.answer(f'Что-то пошло не так... Код ошибки: {response.status_code}')
        return
    faces = response['result']['faces']
    if not faces:
        await state.finish()
        await message.answer('Не удалось распознать лицо')
        return
    current_state = await state.get_state()
    if current_state == FaceSimilarityState.send_photo_1.state:
        await state.update_data(send_photo_1=faces[0]['face_id'])
        await FaceSimilarityState.send_photo_2.set()
        await message.answer(
            'Отправьте мне картинку либо ссылку на неё',
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        async with state.proxy() as data:
            face_1 = data['send_photo_1']
        face_2 = faces[0]['face_id']
        response = ImaggaFaceSimilarityEndpoint(
            message.bot['config']['imagga_api_key'],
            message.bot['config']['imagga_api_secret']
        ).get_face_similarity_data(
            face_1,
            face_2
        )
        if not imagga_success_response(response):
            await message.answer(f'Что-то пошло не так... Код ошибки: {response.status_code}')
            return
        percent = response['result']['score']
        await message.answer(f'Лица похожи друг на друга на {percent}%')


@dp.message_handler(content_types=[ContentType.TEXT], state=[FaceSimilarityState.send_photo_1,
                                                             FaceSimilarityState.send_photo_2])
async def get_photo_object(message: Message, state: FSMContext):
    if not http_link_validator(message.text) or not photo_format_validator(message.text):
        await message.answer('Дурак-простак, введи прямую ссылку на файл')
        return
    loader = ImaggaFaceDetectionsEndpoint(
        message.bot['config']['imagga_api_key'],
        message.bot['config']['imagga_api_secret']
    )
    await message.answer(
        'Фото обрабатывается...',
        reply_markup=START_COMMANDS_KEYBOARD
    )
    response = loader.send_photo_url(message.text)
    if not imagga_success_response(response):
        await state.finish()
        await message.answer(f'Что-то пошло не так... Код ошибки: {response.status_code}')
        return
    faces = response['result']['faces']
    if not faces:
        await state.finish()
        await message.answer('Не удалось распознать лицо')
        return
    current_state = await state.get_state()
    if current_state == FaceSimilarityState.send_photo_1.state:
        await state.update_data(send_photo_1=faces[0]['face_id'])
        await FaceSimilarityState.send_photo_2.set()
        await message.answer(
            'Отправьте мне картинку либо ссылку на неё',
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        async with state.proxy() as data:
            face_1 = data['send_photo_1']
        face_2 = faces[0]['face_id']
        response = ImaggaFaceSimilarityEndpoint(
            message.bot['config']['imagga_api_key'],
            message.bot['config']['imagga_api_secret']
        ).get_face_similarity_data(
            face_1,
            face_2
        )
        if not imagga_success_response(response):
            await message.answer(f'Что-то пошло не так... Код ошибки: {response.status_code}')
            return
        percent = response['result']['score']
        await message.answer(f'Лица похожи друг на друга на {percent}%')
