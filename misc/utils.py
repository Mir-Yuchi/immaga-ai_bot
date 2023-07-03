from datetime import datetime

from requests import Response

from config import IMAGGA_PHOTOS_DIR


def get_file_format(filepath: str) -> str:
    return filepath.split('.')[-1]


def photo_today_file_path(date_obj: datetime, filepath: str) -> str:
    file_format = get_file_format(filepath)
    return f'{IMAGGA_PHOTOS_DIR}/{date_obj.date()}/' \
           f'photo_{date_obj.time().__str__().replace(":", "-")}.{file_format}'


def http_link_validator(text: str) -> bool:
    return text.startswith(('http:', 'https:'))


def photo_format_validator(text: str) -> bool:
    return text.split('.')[-1].lower() in ['jpg', 'png', 'jpeg']


def imagga_success_response(response: Response) -> bool:
    return not isinstance(response, (int, str))
