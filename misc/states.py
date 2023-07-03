from aiogram.dispatcher.filters.state import StatesGroup, State


class GetPhotoObjectState(StatesGroup):
    send_photo = State()


class ScanQRState(StatesGroup):
    send_photo = State()


class ScanColorsState(StatesGroup):
    send_photo = State()


class FaceSimilarityState(StatesGroup):
    send_photo_1 = State()
    send_photo_2 = State()
