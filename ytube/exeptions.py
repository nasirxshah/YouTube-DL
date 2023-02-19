

class YTubeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class RegexMatchError(YTubeException):
    pass


class StreamFilterError(YTubeException):
    pass


class PlayablityError(YTubeException):
    def __init__(self, videoId: str) -> None:
        super().__init__(videoId)


class LoginRequiredError(PlayablityError):
    pass


class VideoUnplayableError(PlayablityError):
    pass


class VideoUnavailable(PlayablityError):
    pass


class LiveStreamError(PlayablityError):
    pass
