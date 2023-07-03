from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import load_config, BASE_DIR

APP_CONFIG: dict = load_config(BASE_DIR / '.env')
storage = MemoryStorage()
bot = Bot(APP_CONFIG['bot_token'])
bot['config']: dict = APP_CONFIG
dp = Dispatcher(bot, storage=storage)
