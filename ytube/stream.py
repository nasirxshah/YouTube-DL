import re
from dataclasses import dataclass, field
from typing import Any

import ytube.exeptions as ex

@dataclass(slots=True)
class Stream:
    url: str = field(init=False)
    itag: int = field(init=False)
    type: str = field(init=False)
    subtype: str = field(init=False)
    video_codec: str | None = None
    audio_codec: str | None = None

    bitrate: int = field(init=False)
    fps: int | None = None
    resolution: int | None = None
    filesize: int | None = field(init=False)

    adaptive: bool | None = None
    progressive: bool | None = None

    def __repr__(self) -> str:
        attrs = ['itag', 'resolution', 'fps', 'bitrate', 'filesize',
                 'type', 'subtype', 'video_codec', 'audio_codec']

        for attr in list(attrs):
            if getattr(self, attr) is None:
                attrs.remove(attr)

        s = ", ".join(map(lambda x: f"{x}={getattr(self, x)}", attrs))
        return f"<Stream: {s}>"



def parseStream(stream: dict[str, Any]) -> Stream:
    s = Stream()
    s.url = stream['url']
    s.itag = stream['itag']

    progessive_pattern = r'(video|audio)/(webm|3gpp|mp4);\scodecs="([a-zA-Z-0-9.]+),\s([a-zA-Z-0-9.]+)"'
    adaptive_pattern = r'(video|audio)/(webm|3gpp|mp4);\scodecs="([a-zA-Z-0-9.]+)"'

    progessive_match = re.search(progessive_pattern, stream['mimeType'])
    if progessive_match:
        s.progressive = True
        s.type, s.subtype, s.video_codec, s.audio_codec = progessive_match.groups()
    else:
        adaptive_match = re.search(adaptive_pattern, stream['mimeType'])
        if adaptive_match:
            s.adaptive = True
            s.type, s.subtype, _codec = adaptive_match.groups()
            if s.type == 'video':
                s.video_codec = _codec
            else:
                s.audio_codec = _codec
        else:
            raise ex.RegexMatchError()

    s.bitrate = stream['bitrate']

    s.filesize = stream.get('contentLength')

    if s.type == "video":
        s.fps = stream['fps']
        s.resolution = int(stream['qualityLabel'][:-1])
    return s
