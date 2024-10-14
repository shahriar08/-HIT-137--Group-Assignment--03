

import tkinter as tk
from tkinter import simpledialog, messagebox

class Song:
    def __init__(self, title, artist, duration):
        # Initialize song attributes
        self.title = title
        self.artist = artist
        self.duration = duration
        self.likes = 0
        self.dislikes = 0
        self.comments = []

    def play(self):
        # Method to play the song
        messagebox.showinfo("Playing", f"Now playing: {self.title} by {self.artist}")

class MyMusic(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Youtube Clone")
        self.geometry("600x400")

        # List of songs
        self.songs = [
            Song("Summer of '69", "Bryan Adams", "3:30"),
            Song("Hotel California", "Eagles", "6:30"),
            Song("It's My Life", "Bon Jovi", "4:15")
        ]

        self.create_widgets()

    def create_widgets(self):
        # Create GUI widgets
        title_label = tk.Label(self, text="Songs")
        title_label.pack()

        # Iterate through songs and create widgets for each
        for song in self.songs:
            song_frame = tk.Frame(self)
            song_frame.pack(pady=5, padx=10, fill=tk.X)

            song_title_label = tk.Label(song_frame, text=song.title, font=("Arial", 12, "bold"))
            song_title_label.pack(anchor=tk.W)

            song_artist_label = tk.Label(song_frame, text=song.artist)
            song_artist_label.pack(anchor=tk.W)

            duration_label = tk.Label(song_frame, text=f"Duration: {song.duration}")
            duration_label.pack(anchor=tk.W)

            # Button to play the song
            play_button = tk.Button(song_frame, text="Play", command=song.play)
            play_button.pack(side=tk.LEFT, padx=5)

            # Button to like the song
            like_button = tk.Button(song_frame, text="Like", command=lambda s=song: self.like_song(s))
            like_button.pack(side=tk.LEFT, padx=5)

            # Button to dislike the song
            dislike_button = tk.Button(song_frame, text="Dislike", command=lambda s=song: self.dislike_song(s))
            dislike_button.pack(side=tk.LEFT, padx=5)

            # Button to comment on the song
            comment_button = tk.Button(song_frame, text="Comment", command=lambda s=song: self.comment_song(s))
            comment_button.pack(side=tk.LEFT, padx=5)

    def like_song(self, song):
        # Method to like the song
        song.likes += 1
        messagebox.showinfo("Liked", f"You liked {song.title}")

    def dislike_song(self, song):
        # Method to dislike the song
        song.dislikes += 1
        messagebox.showinfo("Disliked", f"You disliked {song.title}")

    def comment_song(self, song):
        # Method to comment on the song
        comment = simpledialog.askstring("Comment", f"Enter your comment for {song.title}:")
        if comment:
            song.comments.append(comment)
            messagebox.showinfo("Commented", "Your comment has been added.")

if __name__ == "__main__":
    app = MyMusic()
    app.mainloop()