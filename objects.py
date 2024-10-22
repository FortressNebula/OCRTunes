import os, shutil, glob

#### USERS ####

class User:
    def __init__(self, name="?", DOB="?", fav_artist="?", fav_genre="?"):
        if name == "library":
            raise ValueError("Username cannot be 'library'!")
        
        self.name = name
        self.DOB = DOB
        self.fav_artist = fav_artist
        self.fav_genre = fav_genre

    # Create a folder for the user in /data/, and store their basic info 
    def serialise (self):
        path = "data/" + self.name
        # if the user folder doesn't already exist, make it
        if not os.path.isdir(path):
            os.makedirs(path)
        # if the user's info.txt file doesn't exist, make it
        if not os.path.isfile(path+ "/info.txt"):
            open(path + "/info.txt", 'w').close()

        # write the user info
        file = open(path + "/info.txt", 'wt')
        file.write(self.name + "\n")
        file.write(self.DOB + "\n")
        file.write(self.fav_artist + "\n")
        file.write(self.fav_genre + "\n")
        file.close()
    
    # function to delete all associated data
    def delete (self):
        shutil.rmtree("data/" + self.name)

    def __str__(self):
        return f"Name: {self.name}, DOB: {self.DOB}, Favourite Artist: {self.fav_artist}, Favourite Genre: {self.fav_genre}"

# Read the contents of the /data/ folder and return the user class
# needs a username!! because this is assuming we don't already know anything
# about the user
def deserialise_user (name):
    path = "data/" + name
    # if the user folder doesn't already exist, throw an error
    if not os.path.isdir(path) or not os.path.isfile(path + "/info.txt"):
        raise FileNotFoundError(f"User with username {name} does not exist!")

    user = User()

    # read the user info
    file = open(path + "/info.txt", 'rt')
    filelines = file.read().splitlines()
    user.name, user.DOB, user.fav_artist, user.fav_genre = filelines
    file.close()

    return user

#### SONG ####
class Song:
    def __init__(self, title, artist, genre, length):
        self.title = title
        self.artist = artist
        self.genre = genre
        self.length = length

    # Convert the song into a text representation
    def __str__(self):
        return f"{self.title}, a {self.genre} song by {self.artist} ({self.length // 60}m{'0' if self.length % 60 < 10 else ''}{self.length % 60})"

    def serialise (self):
        return f"{self.title} | {self.artist} | {self.genre} | {self.length // 60}m{'0' if self.length % 60 < 10 else ''}{self.length % 60}"

# Takes a single line of text and returns the corresponding song
def deserialise_song(line):
    data = line.split(' | ')
    time_components = data[3].split('m')

    return Song(data[0], data[1], data[2], int(time_components[0]) * 60 + int(time_components[1]))

# Converts the song library into a list of songs the 
# code can interact with.
def read_all_songs():
    file = open("data/library.txt", 'rt')
    filelines = file.read().splitlines()
    file.close()

    output_array = []
    for line in filelines:
        output_array.append(deserialise_song(line))

    return output_array

#### PLAYLIST ####
class Playlist:
    def __init__(self, name):
        self.list_of_songs = []
        self.name = name

    def add_song(self, song):
        if song in self.list_of_songs:
            self.list_of_songs.remove(song)
        else:
            self.list_of_songs.append(song)

    # Save the playlist under a user 
    def serialise(self, username):
        if not os.path.isdir("data/" + username):
            raise FileNotFoundError(f"User with username {username} does not exist!")

        file = open(f"data/{username}/playlist_{self.name}.txt", 'w')
        file.write(self.name + "\n")
        for song in self.list_of_songs:
            file.write(song.serialise() + "\n")

        file.close()

# Read a playlist from a file
def deserialise_playlist(filename):
    file = open(filename, 'rt')
    filelines = file.read().splitlines()
    file.close()

    out = Playlist("None")
    for index, data in enumerate(filelines):
        if index == 0:
            out.name = data
        elif data != "":
            out.add_song(deserialise_song(data))

    return out

# Read all playlist from a user folder
def deserialise_all_playlists (username):
    directories = glob.glob("data/" + username + "/playlist_*.txt")
    out = []

    for directory in directories:
        out.append(deserialise_playlist(directory))
    
    return out