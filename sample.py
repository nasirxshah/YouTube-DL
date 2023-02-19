from ytube.download import YoutubeDownloader
from ytube.yt import YouTube


yt = YouTube()
player = yt.watch("-OTc0Ki7Sv0")

stream = player.getStreams().getBestQuality(
    progressive=True, subtype="mp4", resolution=360)

if stream:
    downloader = YoutubeDownloader()
    downloader.download(stream.url, f"./{player.getMetaData().title}.mp4")
