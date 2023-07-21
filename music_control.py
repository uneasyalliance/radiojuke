import os
import tkinter as tk
from pathlib import Path
from time import time


# default stream selection:
# music_streams.txt has all streams available, one per line
# current_stream.txt has a digit representing the current stream (counting from zero)
# if current_stream.txt is missing or old (definition TBD) the first stream is the default
# 'old' here may mean more than an hour old.
# there could be day-of-week based defaults in the code

stream_name_file = "music_streams.txt"
cur_stream_file = "current_stream.txt"
stale_cur_stream_time_s = 3600

class Stream:
    def __init__(self, name, url):
        self.name = name.strip()
        self.url = url.strip()


class StreamSelection:
    def __init__(self, path):
        self.streams = []
        self._i_current_stream = 0
        self._stream_name_file = path / stream_name_file
        self._cur_stream_file = path / cur_stream_file

    def read_streams(self):
        with open(self._stream_name_file, 'r', encoding="utf-8") as f:
            for line in f:
                try:
                    (name, url) = line.split(",")
                except ValueError:
                    self.streams.append(None)
                    continue
                self.streams.append(Stream(name=name, url=url))

    def read_cur_stream_idx(self):
        try:
            with open(self._cur_stream_file, 'r', encoding="utf-8") as f:
                self._i_current_stream = int( f.read().strip() )
        except Exception as ex:
            self._i_current_stream = 0
            print(ex)

    def write_cur_stream_idx(self, i):
        try:
            with open(self._cur_stream_file, 'w', encoding="utf-8") as f:
                f.write(str(i))
                f.write("\n")
                self._i_current_stream = i
        except Exception as ex:
            self._i_current_stream = 0
            print(ex)

    def get_cur_stream(self):
        if os.path.exists(self._cur_stream_file):
            if time() - os.path.getmtime(self._cur_stream_file) > stale_cur_stream_time_s:
                # old stream selection, default to first stream
                self.change_cur_stream(0)
            else:
                self.read_cur_stream_idx()
                    
        return self.streams[self._i_current_stream]
                    
    def change_cur_stream(self, i):
        self.write_cur_stream_idx(i)

    
application_path = path=Path( os.path.abspath(__file__) ).parent.resolve()
selection = StreamSelection(application_path)
selection.read_streams()

stream = selection.get_cur_stream()
print("name:", stream.name)
print("url:", stream.url)
