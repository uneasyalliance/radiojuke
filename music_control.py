import os
import tkinter as tk
import tkinter.font
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

application_path = Path( os.path.abspath(__file__) ).parent.resolve()
medium_font_increase = 15
large_font_increase = 30

class Stream:
    def __init__(self, index, name, url):
        self.index = index
        self.name = name.strip()
        self.url = url.strip()


class StreamSelector:
    def __init__(self, path):
        self.streams = []
        self._i_current_stream = 0
        self._stream_name_file = path / stream_name_file
        self._cur_stream_file = path / cur_stream_file

    def read_streams(self):
        with open(self._stream_name_file, 'r', encoding="utf-8") as f:
            index = 0
            for line in f:
                if len(line) > 0 and line[0] != '#': # commented out line
                    try:
                        (name, url) = line.split(",")
                    except ValueError:
                        continue
                    self.streams.append(Stream(index=index, name=name, url=url))
                    index += 1

    def _read_cur_stream_idx(self):
        try:
            with open(self._cur_stream_file, 'r', encoding="utf-8") as f:
                self._i_current_stream = int( f.read().strip() )
        except Exception as ex:
            self._i_current_stream = 0
            print(ex) # TODO log

        return self._i_current_stream

    def _write_cur_stream_idx(self, i):
        try:
            with open(self._cur_stream_file, 'w', encoding="utf-8") as f:
                f.write(str(i))
                f.write("\n")
                self._i_current_stream = i
        except Exception as ex:
            self._i_current_stream = 0
            print(ex) # TODO log

    def get_cur_stream(self):
        if os.path.exists(self._cur_stream_file):
            if time() - os.path.getmtime(self._cur_stream_file) > stale_cur_stream_time_s:
                # old stream selection, default to first stream
                self.change_cur_stream(0)
            else:
                self._read_cur_stream_idx()
                    
        return self.streams[self._i_current_stream]
                    
    def change_cur_stream(self, i):
        self._write_cur_stream_idx(i)

    
class StreamUI:
    def __init__(self, master, selector):
        self.master = master
        self.selector = selector
        self._stream_var = tk.IntVar()
        master.title("Music Player")
        master.resizable(False, False)

    def create(self):
        default_font = tkinter.font.Font(font='TkDefaultFont')
        large_font = medium_font = default_font
        medium_font['size'] += medium_font_increase
        large_font['size'] += large_font_increase

        stream = self.selector.get_cur_stream()
        self._stream_var.set(stream.index)
        self._stream_var.trace('w', self._stream_changed)
        for stream in self.selector.streams:
            btn = tk.Radiobutton(self.master, text=stream.name, variable=self._stream_var, value=stream.index, font=large_font)
            btn.pack(anchor='w', padx=30, pady=10)

    def _stream_changed(self, *_):
        self.selector.change_cur_stream(self._stream_var.get())


def main():            
    selector = StreamSelector(application_path)
    selector.read_streams()

    root = tk.Tk()

    ui = StreamUI(master=root, selector=selector)
    ui.create()
    root.mainloop()


if __name__ == "__main__":
    main()
