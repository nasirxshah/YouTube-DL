from ytube.auth import YTubeToken
from ytube.innertube import InnerTube
from ytube.player import Player
from ytube.request import Request
from ytube.extract import Extractor


class YouTube:
    def __init__(self, proxy:dict|None=None) -> None:
        self.request = Request(proxy=proxy)
        self.innertube = InnerTube(client="ANDROID", request=self.request)

        self.watched: dict[str, Player] = {}

    def watch(self, url) -> Player:
        video_id = Extractor.videoId(url)

        if video_id in self.watched:
            return self.watched[video_id]
        else:
            player = Player(video_id, self.innertube)
            self.watched[video_id] = player
            return player

    def login(self, username: str, persistent=True):
        session = YTubeToken(username, self.request, persistent=persistent)
        if session.auth is None:
            session.generate()

        self.innertube.auth = session.auth
