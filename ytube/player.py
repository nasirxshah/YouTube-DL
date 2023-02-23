import ytube.exeptions as ex
from ytube.innertube import InnerTube
from ytube.metadata import parseMetaData
from ytube.query import StreamQuery
from ytube.stream import parseStream,Stream
from ytube.download import DownLoader

class Player:
    def __init__(self, video_id: str, innertube: InnerTube) -> None:
        self.video_id = video_id
        self.vidinfo = innertube.player(self.video_id)
        self._check_playable()

        self._streams = None
        self._captions = None
        self._metadata = None

    @property
    def captions(self):
        if self._captions:
            return self._captions

    @property
    def metadata(self):
        if self._metadata:
            return self._metadata
        
        self._metadata = parseMetaData(self.vidinfo['videoDetails'])
        return self._metadata

    @property
    def streams(self):
        if self._streams:
            return self._streams
        
        streams = []
        for stream in self.vidinfo['streamingData']['formats']:
            streams.append(parseStream(stream))

        for stream in self.vidinfo['streamingData']['adaptiveFormats']:
            streams.append(parseStream(stream))

        self._streams = StreamQuery(streams)
        return self._streams

    def _check_playable(self):
        status = self.vidinfo['playabilityStatus']['status']

        if status == 'UNPLAYABLE':
            raise ex.VideoUnplayableError(self.video_id)

        elif status == 'LOGIN_REQUIRED':
            raise ex.LoginRequiredError(self.video_id)

        elif status == 'ERROR':
            raise ex.VideoUnavailable(self.video_id)

        elif status == 'LIVE_STREAM':
            raise ex.LiveStreamError(self.video_id)
        
    def download(self, stream:Stream, filepath:str="."):
        dl = DownLoader(self.metadata.title,stream.subtype,stream.url)
        dl.start(filepath)
    

