from aiogram.types import KeyboardButton

from commands import Commands


GET_PHOTO_OBJ = KeyboardButton(Commands.get_obj.value)
BARCODE_SCAN_BUTTON = KeyboardButton(Commands.barcodes.value)
COLORS_SCAN_BUTTON = KeyboardButton(Commands.colors.value)
FACE_SIMILARITY_BUTTON = KeyboardButton(Commands.face_similarity.value)
