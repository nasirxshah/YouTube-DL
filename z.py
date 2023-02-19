from ytube.yt import YouTube
url = "https://youtube.com/watch?v=EX_8ZjT2sO4"

yt = YouTube()
yt.login("nasir.ciem.it")
player = yt.watch(url)
meta = player.getMetaData()
print(meta)
