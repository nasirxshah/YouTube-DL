import ytube.exeptions as ex
from ytube.innertube import InnerTube
from ytube.metadata import parseMetaData
from ytube.query import StreamQuery
from ytube.stream import parseStream,Stream

class Player:
    def __init__(self, video_id: str, innertube: InnerTube) -> None:
        self.video_id = video_id
        self.vidinfo = innertube.player(self.video_id)
        self.request = innertube.request
        self._check_playable()

    def getCaptions(self):
        pass

    def getMetaData(self):
        metadata = parseMetaData(self.vidinfo['videoDetails'])
        return metadata

    def getStreams(self):
        streams = []
        for stream in self.vidinfo['streamingData']['formats']:
            streams.append(parseStream(stream))
        for stream in self.vidinfo['streamingData']['adaptiveFormats']:
            streams.append(parseStream(stream))

        return StreamQuery(streams)

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
        metadata = self.getMetaData()
        with open(f"{filepath}/{metadata.title}.{stream.subtype}",'wb') as fp:
            for content in self.request.stream(stream.url):
                fp.write(content)