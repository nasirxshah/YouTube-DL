from ytube.request import Request


class DownLoader:
    RANGE_SIZE = 10*1024*1024 #10MB
    CHUNK_SIZE = 128*1024 #128 KB

    def __init__(self,title:str,extension:str,stream_url:str) -> None:
        self.title = title
        self.extension = extension
        self.stream_url = stream_url

        self.request = Request()
        self.spinner = Spinner()
        self.downloaded = 0

    def start(self, path:str = "."):
        self.spinner.spin()
        with open(f"{path}/{self.title}.{self.extension}","wb") as fp:
            for content in self.request.stream(self.stream_url, downrange=self.RANGE_SIZE):
                fp.write(content)
                self.onprogress()

        self.oncomplete()

    def onprogress(self):
        self.downloaded += self.CHUNK_SIZE
        self.spinner.text = f"{self.title} {self.downloaded/(1024*1024)} MB"

    def oncomplete(self):
        self.spinner.stop()


import time
from itertools import cycle
import threading

class Spinner:
    default_frames = ['⢀⠀',
                                          '⡀⠀',
                                          '⠄⠀',
                                          '⢂⠀',
                                          '⡂⠀',
                                          '⠅⠀',
                                          '⢃⠀',
                                          '⡃⠀',
                                          '⠍⠀',
                                          '⢋⠀',
                                          '⡋⠀',
                                          '⠍⠁',
                                          '⢋⠁',
                                          '⡋⠁',
                                          '⠍⠉',
                                          '⠋⠉',
                                          '⠋⠉',
                                          '⠉⠙',
                                          '⠉⠙',
                                          '⠉⠩',
                                          '⠈⢙',
                                          '⠈⡙',
                                          '⢈⠩',
                                          '⡀⢙',
                                          '⠄⡙',
                                          '⢂⠩',
                                          '⡂⢘',
                                          '⠅⡘',
                                          '⢃⠨',
                                          '⡃⢐',
                                          '⠍⡐',
                                          '⢋⠠',
                                          '⡋⢀',
                                          '⠍⡁',
                                          '⢋⠁',
                                          '⡋⠁',
                                          '⠍⠉',
                                          '⠋⠉',
                                          '⠋⠉',
                                          '⠉⠙',
                                          '⠉⠙',
                                          '⠉⠩',
                                          '⠈⢙',
                                          '⠈⡙',
                                          '⠈⠩',
                                          '⠀⢙',
                                          '⠀⡙',
                                          '⠀⠩',
                                          '⠀⢘',
                                          '⠀⡘',
                                          '⠀⠨',
                                          '⠀⢐',
                                          '⠀⡐',
                                          '⠀⠠',
                                          '⠀⢀',
                                          '⠀⡀']
    default_interval = 80 #ms

    def __init__(self) -> None:
        self.frames = cycle(self.default_frames)
        self.interval = 0.001 * self.default_interval
        self._screen_lock = threading.Lock()

        self.text = ""

    def spin(self):
        self._spinning = True
        time.sleep(self.interval)
        self._screen_lock.acquire()
        self._stop_flag = False

        def inner(spinner: Spinner):
            while spinner._stop_flag is False:
                print(
                    f"\r{next(spinner.frames)} {spinner.text}", end="")
                time.sleep(spinner.interval)

            spinner._screen_lock.release()
            spinner._spinning = False

        thread = threading.Thread(
            target=inner, args=(self,), daemon=True)
        thread.start()

    def stop(self):
        self._stop_flag = True
        print("\r", end="")