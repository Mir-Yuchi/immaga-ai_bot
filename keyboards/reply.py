from aiogram.types import ReplyKeyboardMarkup

from buttons.reply import (
    GET_PHOTO_OBJ, BARCODE_SCAN_BUTTON,
    COLORS_SCAN_BUTTON, FACE_SIMILARITY_BUTTON
)

START_COMMANDS_KEYBOARD = ReplyKeyboardMarkup([
    [GET_PHOTO_OBJ, BARCODE_SCAN_BUTTON],
    [COLORS_SCAN_BUTTON, FACE_SIMILARITY_BUTTON]
], resize_keyboard=True)
