import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR / 'media'
IMAGGA_PHOTOS_DIR = MEDIA_DIR / 'imagga'


def load_config(env_path: str) -> dict:
    load_dotenv(env_path)
    if not os.path.exists(IMAGGA_PHOTOS_DIR):
        os.makedirs(IMAGGA_PHOTOS_DIR)
    return {
        'bot_token': os.getenv('BOT_TOKEN'),
        'imagga_api_key': os.getenv('IMAGGA_API_KEY'),
        'imagga_api_secret': os.getenv('IMAGGA_API_SECRET'),
    }
