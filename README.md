## API USAGE

``` python
from ytube.downloader import DownLoader
from ytube import YouTube

yt = YouTube()
player = yt.watch("https://youtu.be/x7X9w_GIm1s")

stream = player.getStreams().getBestQuality(progressive=True, subtype="mp4", resolution=360)

metadata = player.getMetaData()


if stream:
    downloader = DownLoader()
    downloader.download(stream.url, f"./{metadata.title}.{stream.subtype}")

```

