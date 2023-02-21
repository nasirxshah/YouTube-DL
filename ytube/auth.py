import os
import time
import pathlib
from requests.auth import HTTPBasicAuth
from ytube.request import Request
import json
from typing import Callable

_cache_dir = pathlib.Path(__file__).parent.resolve() / '__cache__'


class YTubeAuth(HTTPBasicAuth):

    def __init__(self, access_token: str, refresh_token: str, expires: int) -> None:
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires = expires

        self.on_expired: Callable | None = None

    def toDict(self) -> dict:
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires": self.expires
        }

    def __call__(self, r):
        assert self.expires is not None
        assert self.access_token is not None

        if self.expires < time.time():
            if self.on_expired:
                self.on_expired()
            else:
                raise Exception()  # TODO

        r.headers['Authorization'] = f'Bearer {self.access_token}'
        return r


class YTubeToken:
    _client_id = '861556708454-d6dlm3lh05idd8npek18k6be8ba3oc68.apps.googleusercontent.com'
    _client_secret = 'SboVhoG9s0rNafixCSGGKXAT'

    def __init__(self, username: str, request: Request, persistent=True) -> None:
        self.request = request
        self.persistent = persistent
        self.token_file = os.path.join(_cache_dir, f'{username}.json')
        self.load()

    def load(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as fp:
                tokens = json.load(fp)
                self.auth = YTubeAuth(
                    tokens['access_token'], tokens['refresh_token'], tokens['expires'])
                self.auth.on_expired = self.refresh
        else:
            self.auth: YTubeAuth | None = None

    def dump(self):
        assert self.auth is not None
        with open(self.token_file, 'w') as fp:
            json.dump(self.auth.toDict(), fp, indent=4)

    def generate(self) -> YTubeAuth:
        data = {
            'client_id': self._client_id,
            'scope': 'https://www.googleapis.com/auth/youtube'
        }

        start_time = time.time() - self.request.timeout

        resp = self._post(
            'https://oauth2.googleapis.com/device/code', data=data)

        verification_url = resp['verification_url']
        user_code = resp['user_code']
        print(f'Please open {verification_url} and input code {user_code}')
        input('Press enter when you have completed this step.')

        data = {
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'device_code': resp['device_code'],
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
        }

        resp = self._post(
            'https://oauth2.googleapis.com/token', data=data)

        self.auth = YTubeAuth(
            resp['access_token'], resp['refresh_token'], start_time + resp['expires_in'])
        self.auth.on_expired = self.refresh

        if self.persistent:
            self.dump()

        return self.auth

    def refresh(self):
        assert self.auth is not None
        data: dict[str, str] = {
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self.auth.refresh_token
        }

        start_time = time.time() - self.request.timeout

        resp = self._post(
            'https://oauth2.googleapis.com/token', data=data)

        self.auth.access_token = resp['access_token']
        self.auth.expires = start_time + resp['expires_in']

        if self.persistent:
            self.dump()

    def _post(self, url: str, params: dict | None = None, data: dict | None = None) -> dict:
        resp = self.request.post(url, params=params, json=data)
        return resp.json()
