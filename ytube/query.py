from typing import Sequence

from ytube.stream import Stream


class StreamQuery:
    def __init__(self, streams: Sequence[Stream]) -> None:
        self.streams = streams

    def filter(self,
               resolution: int | None = None,
               fps: int | None = None,
               type: str | None = None,
               subtype: str | None = None,
               video_codec: str | None = None,
               audio_codec: str | None = None,
               adaptive: bool | None = None,
               progressive: bool | None = None,
               ):

        lamdas = []

        if resolution is not None:
            lamdas.append(lambda x: x.resolution == resolution)

        if fps is not None:
            lamdas.append(lambda x: x.fps == fps)
        if type is not None:
            lamdas.append(lambda x: x.type == type)
        if subtype is not None:
            lamdas.append(lambda x: x.subtype == subtype)
        if video_codec is not None:
            lamdas.append(lambda x: x.video_codec == video_codec)
        if audio_codec is not None:
            lamdas.append(lambda x: x.audio_codec == audio_codec)
        if adaptive is not None:
            lamdas.append(lambda x: x.adaptive == adaptive)
        if progressive is not None:
            lamdas.append(lambda x: x.progressive == progressive)

        _streams = list(self.streams)
        for func in lamdas:
            _streams = list(filter(func, _streams))

        orders = ['resolution', 'fps', 'bitrate']
        if type == "audio" and adaptive == True:
            orders = ['bitrate']

        return StreamQuery(_streams).orderby(*orders)

    def orderby(self, *attrs):
        _streams = list(self.streams)
        for attr in reversed(attrs):
            _streams = filter(lambda x: getattr(x, attr)
                              is not None, _streams)
            _streams = sorted(_streams,
                              key=lambda x: getattr(x, attr))

        return StreamQuery(_streams)


    def __iter__(self):
        return iter(self.streams)

    def __len__(self):
        return len(self.streams)

    def __getitem__(self, i):
        return self.streams[i]

    def __repr__(self) -> str:

        return f"<StreamQuery: {list(self.streams)}>" if isinstance(self.streams, filter) else f"<StreamQuery: {self.streams}>"
