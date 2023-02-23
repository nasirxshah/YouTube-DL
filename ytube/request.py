import logging

import requests

logger = logging.getLogger(__name__)


class Request:
    _default_timeout = 10  # in second

    def __init__(self, proxy:dict|None=None,debug=False) -> None:
        self.debug = debug
        self._session = requests.Session()
        self._user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        self.timeout = self._default_timeout
        self.proxy = proxy

    def get(self, url: str, params: dict | None = None):
        req = requests.Request("GET", url, params=params)
        return self.send(req)

    def post(self, url: str, params: dict | None = None, data: dict | None = None, json: dict | None = None):
        req = requests.Request(
            "POST", url, params=params, json=json, data=data)
        return self.send(req)

    def stream(self, url: str, params: dict | None = None, downrange:int = 1024*1024):

        file_size = downrange = downrange
        downloaded = 0
        
        while file_size >= downloaded + downrange:
            headers = {
                "Range": f"bytes={downloaded}-{downloaded + downrange - 1}"
            }
            req = requests.Request("GET", url, params=params,headers=headers)
            resp = self.send(req, stream=True)
            for content in resp.iter_content(chunk_size=128*1024):
                yield content

            file_size = int(resp.headers["Content-Range"].split("/")[1])
            if file_size > downloaded + downrange:
                downloaded += downrange
            



    def send(self, req: requests.Request, **kwargs):
        req.headers["User-Agent"] = self._user_agent
        prepped = self._session.prepare_request(req)

        if self.debug:
            logger.debug(
                f"Request: {req.method} {req.url} {req.params} {req.headers}")

        try:
            resp = self._session.send(prepped, timeout=self.timeout,proxies=self.proxy, **kwargs)
        except requests.RequestException as e:
            raise e

        if self.debug:
            logger.debug(f"Response: {resp.status_code} {resp.headers}")

        return resp
