import tkinter as tk
from tkinter import filedialog
#import mpv


class AudioPlayer:
    def __init__(self, master):
        self.master = master
        master.title("Audio Player")

        # Create radio buttons for stream selection
        self.stream_var = tk.StringVar()
        self.stream_var.set("stream1")
        self.stream1_radio = tk.Radiobutton(master, text="Stream 1", variable=self.stream_var, value="stream1")
        self.stream1_radio.pack()
        self.stream2_radio = tk.Radiobutton(master, text="Stream 2", variable=self.stream_var, value="stream2")
        self.stream2_radio.pack()

        # Create buttons for actions
        self.play_button = tk.Button(master, text="Play", command=self.play_audio)
        self.play_button.pack()
        self.stop_button = tk.Button(master, text="Stop", command=self.stop_audio)
        self.stop_button.pack()
        self.browse_button = tk.Button(master, text="Browse", command=self.browse_file)
        self.browse_button.pack()

        # Create mpv player instance
        #self.player = mpv.MPV()

        # Store the currently playing stream or file
        self.current_stream = None

    def play_audio(self):
        selection = self.stream_var.get()
        if selection == "stream1":
            url = "http://stream1.example.com/stream"
            self.play_stream(url)
        elif selection == "stream2":
            url = "http://stream2.example.com/stream"
            self.play_stream(url)
        elif self.current_stream is None:
            tk.messagebox.showwarning("Error", "No audio selected!")
            return

    def play_stream(self, url):
        if self.current_stream is not None:
            self.stop_audio()
        #self.player.play(url)
        self.current_stream = url

    def stop_audio(self):
        if self.current_stream is not None:
            #self.player.stop()
            self.current_stream = None

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
        if file_path:
            if self.current_stream is not None:
                self.stop_audio()
            #self.player.play(file_path)
            self.current_stream = file_path

root = tk.Tk()
audio_player = AudioPlayer(root)
root.mainloop()
