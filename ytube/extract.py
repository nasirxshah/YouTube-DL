import re
import ytube.exeptions as ex

class Extractor:
    @staticmethod
    def videoId(url) -> str:
        watch_pattern = r"(https://)?(www.)?youtube.com/watch\?v=(?P<video_id>[0-9A-Za-z_-]{11}).*"
        short_pattern = r"(https://)?youtu.be/(?P<video_id>[0-9A-Za-z_-]{11}).*"
        embed_pattern = r"(https://)?(www.)?youtube.com/embed/(?P<video_id>[0-9A-Za-z_-]{11}).*"

        mathced = re.match(watch_pattern, url)
        if mathced:
            video_id = mathced.groupdict()['video_id']
            return video_id

        mathced = re.match(short_pattern, url)
        if mathced:
            video_id = mathced.groupdict()['video_id']
            return video_id

        mathced = re.match(embed_pattern, url)
        if mathced:
            video_id = mathced.groupdict()['video_id']
            return video_id
        raise ex.RegexMatchError()
