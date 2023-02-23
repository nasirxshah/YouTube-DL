## API USAGE

``` python
from ytube import YouTube

yt = YouTube()
player = yt.watch("https://youtu.be/x7X9w_GIm1s")

streams = player.streams.filter(progressive=True)
if streams:
    player.download(streams[-1],".")

```

