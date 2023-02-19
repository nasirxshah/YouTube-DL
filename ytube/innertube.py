import urllib.parse
from typing import Any

import requests

from ytube.auth import YTubeAuth
from ytube.request import Request


class InnerTube:
    _DEFAULT_URL = 'https://www.youtube.com'

    _routes = {
        "yt.player": "/youtubei/v1/player",
        "yt.search": "/youtubei/v1/search",
        "yt.verify.age": "/youtubei/v1/verify_age",
        "yt.transcript": "/youtubei/v1/get_transcript",
    }
    _default_api_keys = 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'

    _deafult_clients = {
        'WEB': {
            'clientName': 'WEB',
            'clientVersion': '2.20200720.00.02'
        },
        'ANDROID': {
            'clientName': 'ANDROID',
            'clientVersion': '16.20'
        },
        'WEB_EMBED': {
            'clientName': 'WEB',
            'clientVersion': '2.20210721.00.00',
            'clientScreen': 'EMBED'
        },
        'ANDROID_EMBED':  {
            'clientName': 'ANDROID',
            'clientVersion': '16.20',
            'clientScreen': 'EMBED'
        }
    }

    def __init__(self,
                 client: str,
                 api_key: str | None = None,
                 auth: YTubeAuth | None = None,
                 request=Request()
                 ) -> None:

        self.api_key = self._default_api_keys if api_key is None else api_key
        self.auth = auth
        self.client = client
        self.request = request

    def player(self, video_id):

        _params = {
            'videoId': video_id,
        }
        return self._post("yt.player", params=_params)

    def _prepare(self, route: str, params: dict | None = None, data: dict | None = None) -> requests.Request:
        uri = urllib.parse.urljoin(self._DEFAULT_URL, self._routes[route])

        _params: dict[str, Any] = {
            'contentCheckOk': True,
            'racyCheckOk': True
        }
        if params is not None:
            _params.update(params)

        if self.auth is None:
            assert self.api_key is not None
            _params['key'] = self.api_key

        # payload
        _data = {
            'context': {
                "client": self._deafult_clients[self.client]
            }
        }

        if data is not None:
            _data.update(data)

        req = requests.Request("POST", uri, params=_params,
                               json=_data, auth=self.auth)

        return req

    def _post(self, route: str, params: dict | None = None, data: dict | None = None):
        prepped = self._prepare(route, params=params, data=data)
        resp = self.request.send(prepped)
        return resp.json()
