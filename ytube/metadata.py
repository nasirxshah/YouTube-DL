from dataclasses import dataclass, field


@dataclass(slots=True)
class MetaData:
    videoId: str = field(init=False)
    title: str = field(init=False)
    duration: int = field(init=False)
    keywords: list[str] = field(init=False)
    channelId: str = field(init=False)
    description: str = field(init=False)
    thumbnail: str = field(init=False)
    author: str = field(init=False)
    viewCount: int = field(init=False)
    allowRatings: bool = field(init=False)
    isPrivate: bool = field(init=False)
    isLiveContent: bool = field(init=False)

    def __repr__(self) -> str:
        attrs = ['videoId', 'title', 'duration', 'author']

        for attr in list(attrs):
            if getattr(self, attr) is None:
                attrs.remove(attr)

        s = ", ".join(map(lambda x: f"{x}={getattr(self, x)}", attrs))
        return f"<MetaData: {s}>"


def parseMetaData(metadata: dict):
    data = MetaData()
    data.videoId = metadata['videoId']
    data.title = metadata['title']
    data.duration = metadata['lengthSeconds']
    data.keywords = metadata['keywords']
    data.channelId = metadata['channelId']
    data.description = metadata['shortDescription']

    data.thumbnail = maxThumbnail(metadata['thumbnail']['thumbnails'])

    data.allowRatings = metadata['allowRatings']
    data.author = metadata['author']
    data.viewCount = metadata['viewCount']
    data.isPrivate = metadata['isPrivate']
    data.isLiveContent = metadata['isLiveContent']

    return data


def maxThumbnail(thumbnails: list[dict]) -> str:
    _max = thumbnails[0]
    for t in thumbnails:
        if t['height']*t['width'] > _max['height']*_max['width']:
            _max = t

    return _max['url']
