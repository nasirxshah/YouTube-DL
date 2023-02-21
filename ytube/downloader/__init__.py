from typing import Callable
from ytube.request import Request
import threading

class DownLoader:
    def __init__(self) -> None:
        self.on_progress: Callable | None = None
        self.on_complete: Callable | None = None
        self.request = Request()

    def download(self, url, file, threaded=False):
        def run():
            with open(file, "wb") as fp:
                for content in self.request.stream(url):
                    fp.write(content)
                    if self.on_progress:
                        self.on_progress(content)

                if self.on_complete:
                    self.on_complete()
                    
        if threaded:
            thread = threading.Thread(target=run)
            thread.start()
        else:
            run()



    def onProgress(self,content):
        pass

    def onComplete(self):
        pass