import os
import tkinter as tk
from pathlib import Path


# default stream selection:
# music_streams.txt has all streams available, one per line
# current_stream.txt has a digit representing the current stream (counting from zero)
# if current_stream.txt is missing or old (definition TBD) the first stream is the default
# 'old' here may mean more than an hour old.
# there could be day-of-week based defaults in the code


class StreamChooser:
    def __init__(self, stream_name_file):
        self.i_current_stream = 0
        self.stream_name_file = stream_name_file
        self.streams = []

    def read_streams(self):
        with open(self.stream_name_file, 'r', encoding="utf-8") as f:
            for line in f:
                line = line.rstrip()
                self.streams.append(line)

    
path = Path( os.path.abspath(__file__) ).parent.resolve()
chooser = StreamChooser(path / "music_streams.txt")
chooser.read_streams()


