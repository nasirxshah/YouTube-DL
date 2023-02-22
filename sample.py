from ytube import YouTube

yt = YouTube()
player = yt.watch("https://youtu.be/x7X9w_GIm1s")


stream = player.getStreams().getBestQuality(adaptive=True, resolution=480)


if stream:
    player.download(stream,".")