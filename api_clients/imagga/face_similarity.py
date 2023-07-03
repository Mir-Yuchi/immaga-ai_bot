from requests import Response

from .base import BaseImaggaManager


class ImaggaFaceSimilarityEndpoint(BaseImaggaManager):

    def __init__(self, api_key: str, api_secret: str, lang: str = 'ru'):
        super().__init__(api_key, api_secret, lang)
        self.FACE_SIMILARITY_BASE_URL = self.API_BASE_URL + '/faces/similarity'

    def get_face_similarity_data(self, face_id: str, second_face_id: str) -> dict | Response:
        response = self.get(
            self.FACE_SIMILARITY_BASE_URL,
            params={
                'face_id': face_id,
                'second_face_id': second_face_id,
                'language': self.lang
            },
            headers=self.headers,
            auth=(self.api_key, self.api_secret)
        )
        if response.status_code == 200:
            return response.json()
        return response
