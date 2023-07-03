from requests import Response

from .base import BaseImaggaManager


class ImaggaBarcodesEndpoint(BaseImaggaManager):

    def __init__(self, api_key: str, api_secret: str, lang: str = 'ru'):
        super().__init__(api_key, api_secret, lang)
        self.API_BARCODES_BASE_URL = self.API_BASE_URL + '/barcodes'

    def send_photo_bytes(self, photo: bytes) -> dict | Response:
        return self.define_photo_request(
            photo,
            self.API_BARCODES_BASE_URL,
        )

    def send_photo_url(self, photo_url: str) -> dict | Response:
        return self.define_photo_request(
            photo_url,
            self.API_BARCODES_BASE_URL,
        )
