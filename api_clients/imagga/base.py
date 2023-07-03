from typing import Union

from requests import Session, Response


class BaseImaggaManager(Session):
    API_BASE_URL = 'https://api.imagga.com/v2'
    headers = {
        'User-Agent': 'I\'m Fake user-agent',
    }

    def __init__(self, api_key: str, api_secret: str, lang: str):
        super().__init__()
        self.__api_key = api_key
        self.__api_secret = api_secret
        self.lang = lang

    @property
    def api_key(self):
        return self.__api_key

    @property
    def api_secret(self):
        return self.__api_secret

    def define_photo_request(self,
                             photo: Union[bytes, str],
                             endpoint_url: str,
                             **params) -> dict | Response | str:
        if isinstance(photo, bytes):
            params['image'] = photo
            params['language'] = self.lang
            response = self.post(
                endpoint_url,
                data=params,
                headers=self.headers,
                auth=(self.api_key, self.api_secret)
            )
        elif isinstance(photo, str):
            params['image_url'] = photo
            params['language'] = self.lang
            response = self.get(
                endpoint_url,
                params=params,
                headers=self.headers,
                auth=(self.api_key, self.api_secret)
            )
        else:
            return 'Bad photo content!'
        if response.status_code in [200, 201]:
            return response.json()
        return response
