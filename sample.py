from ytube import YouTube

yt = YouTube()
player = yt.watch("https://youtu.be/x7X9w_GIm1s")


stream = player.streams.getBestQuality(progressive=True, resolution=720)


if stream:
    player.download(stream,".")
