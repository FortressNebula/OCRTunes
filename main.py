from objects import *
from gui import *
import random

class TunesData:
    def __init__(self):
        self.song_library = read_all_songs()
        self.song_library.sort(key=lambda song : ord(song.title[0]))
        self.state = "TITLE"
        self.running = True
        self.input_binds = {}
        self.current_user = None
        self.current_building_playlist = None
    
    def set_state (self, newstate):
        self.state = newstate
        self.current_building_playlist = None

    def exit (self):
        self.running = False
    
    def log_out (self):
        self.state = 'TITLE'
        self.current_user = None

data = TunesData()

# CONTROL
def reset_input_binds ():
    data.input_binds = {
        "exit" : lambda : data.exit()
    }

def bind_input (input_string, trigger):
    data.input_binds[input_string] = trigger

def parse_input ():
    received = input("> ")
    if received in data.input_binds:
        data.input_binds[received]()
    else:
        print("INVALID")
    return received

#region LOGIN AND SIGNUP AND MAIN
def state_title ():
    reset_input_binds()
    
    gui = """   ____   _____ _____    _______                    
  / __ \ / ____|  __ \  |__   __|                   
 | |  | | |    | |__) |    | |_   _ _ __   ___  ___ 
 | |  | | |    |  _  /     | | | | | '_ \ / _ \/ __|
 | |__| | |____| | \ \     | | |_| | | | |  __/\__ \\
  \____/ \_____|_|  \_\    |_|\__,_|_| |_|\___||___/""".splitlines()
    gui.append(' ')
    gui.append('<centre>')
    gui.append('1. Log in')
    gui.append(' ')
    gui.append('2. Sign up')
    gui.append('<centre>')

    draw_gui_aligned(gui, 5)

    bind_input('1', lambda : data.set_state('LOGIN'))
    bind_input('2', lambda : data.set_state('SIGNUP'))

    parse_input()

def state_login ():
    reset_input_binds()

    gui = """  _                   _       
 | |                 (_)      
 | |     ___   __ _   _ _ __  
 | |    / _ \ / _` | | | '_ \ 
 | |___| (_) | (_| | | | | | |
 |______\___/ \__, | |_|_| |_|
               __/ |          
              |___/           """.splitlines()
    gui.append('<centre>')
    gui.append(' ')
    gui.append('Enter your username: ')
    gui.append('<centre>')

    draw_gui_aligned(gui, 5)
    username = input("> ")
    succeeded = True

    try:
        data.current_user = deserialise_user(username)
    except FileNotFoundError:
        succeeded = False
    
    if not succeeded:
        print("USER NOT FOUND")
        data.set_state("TITLE")
    else:
        print("SUCCESS")
        data.set_state("MAIN")

def state_signup ():
    reset_input_binds()

    gui = """   _____ _                           
  / ____(_)                          
 | (___  _  __ _ _ __    _   _ _ __  
  \___ \| |/ _` | '_ \  | | | | '_ \ 
  ____) | | (_| | | | | | |_| | |_) |
 |_____/|_|\__, |_| |_|  \__,_| .__/ 
            __/ |             | |    
           |___/              |_|    """.splitlines()
    gui.append('<centre>')
    gui.append(' ')
    gui.append('Just a few questions and you\'ll be on you\'re way!')
    gui.append('<centre>')

    questions = ["name", "date of birth", "favourite artist", "favourite genre"]
    answers = []

    for index, question in enumerate(questions):
        addition = [' ']
        addition.append("[" + str(index+1) + "/4]")
        addition.append('<centre>')
        addition.append(' ')
        addition.append(f"Enter your {question}:")
        addition.append('<centre>')

        draw_gui_aligned(gui + addition, 5)
        answers.append(input('> '))

    data.current_user = User(answers[0], answers[1], answers[2], answers[3])
    data.current_user.serialise()

    data.set_state('MAIN')

def state_main ():
    reset_input_binds()

    # requires current user to be present
    gui = ["Hello, " + data.current_user.name + "!"]
    gui.append(' ')
    gui.append('<left>')
    gui += """   ____   _____ _____    _______                    
  / __ \ / ____|  __ \  |__   __|                   
 | |  | | |    | |__) |    | |_   _ _ __   ___  ___ 
 | |  | | |    |  _  /     | | | | | '_ \ / _ \/ __|
 | |__| | |____| | \ \     | | |_| | | | |  __/\__ \\
  \____/ \_____|_|  \_\    |_|\__,_|_| |_|\___||___/""".splitlines()
    gui.append('<centre>')
    gui.append(' ')
    gui.append('1. Edit details')
    gui.append(' ')
    gui.append('2. Song library')    
    gui.append(' ')
    gui.append('3. Playlists')    
    gui.append(' ')
    gui.append('4. Log out')
    gui.append('<centre>')

    draw_gui_aligned(gui, 5)

    bind_input('1', lambda : data.set_state('EDIT'))
    bind_input('2', lambda : data.set_state('SONGS'))
    bind_input('3', lambda : data.set_state('PLAYLIST'))
    bind_input('4', lambda : data.log_out())

    parse_input()
#endregion

def show_playlist (playlist:Playlist, title:list):
    gui = ["Type anything to go back ..."]
    gui.append(' ')
    gui.append('<left>')
    gui += title
    gui.append('<centre>')
    gui.append(' ')
    gui.append('Looking at: ' + playlist.name)
    gui.append('<centre>')
    gui.append(' ')

    for song in playlist.list_of_songs:
        gui.append(str(song))
        gui.append(' ')
    
    gui.append('<centre>')

    draw_gui_aligned(gui, 5)

    input("> ")

def make_show_playlist_lambda (playlist, title):
    return lambda : show_playlist(playlist, title)

def state_playlist_launchpad():
    reset_input_binds()
    
    gui = ["Type '1' to exit ..."]
    gui.append(' ')
    gui.append('<left>')
    title = """  _____  _             _ _     _       
 |  __ \| |           | (_)   | |      
 | |__) | | __ _ _   _| |_ ___| |_ ___ 
 |  ___/| |/ _` | | | | | / __| __/ __|
 | |    | | (_| | |_| | | \__ \ |_\__ \\
 |_|    |_|\__,_|\__, |_|_|___/\__|___/
                  __/ |                
                 |___/                 """.splitlines()
    gui += title
    gui.append('<centre>')
    gui.append('')
    gui.append('2. Create new playlist')
    gui.append('3. Generate new playlist')
    gui.append('<centre>')
    gui.append(' ')
    gui.append(' - VIEW PLAYLISTS -')
    gui.append(' ')
    gui.append('<centre>')

    for index, playlist in enumerate(deserialise_all_playlists(data.current_user.name)):
        gui.append(f"{index + 4}. {playlist.name}")
        gui.append(' ')

        bind_input(str(index + 4), make_show_playlist_lambda(playlist, title))
    
    gui.append('<centre>')

    draw_gui_aligned(gui, 5)

    bind_input('1', lambda : data.set_state("MAIN"))
    bind_input('2', lambda : data.set_state("PLAYLIST_CREATE"))
    bind_input('3', lambda : data.set_state("PLAYLIST_GENERATE"))

    parse_input()

def create_playlist_and_switch ():
    data.current_building_playlist.serialise(data.current_user.name)
    data.current_building_playlist = None
    data.set_state("PLAYLIST")

def make_playlist_lambda (index):
    return lambda : data.current_building_playlist.add_song(data.song_library[index])

def state_create_playlist ():
    reset_input_binds()

    if data.current_building_playlist == None:
        data.current_building_playlist = Playlist(input("Enter playlist name > "))
    
    gui = ["Type '1' to confirm ..."]
    gui.append("Type '2' to exit ...")
    gui.append(' ')
    gui.append('<left>')
    title = """  _____  _             _ _     _       
 |  __ \| |           | (_)   | |      
 | |__) | | __ _ _   _| |_ ___| |_ ___ 
 |  ___/| |/ _` | | | | | / __| __/ __|
 | |    | | (_| | |_| | | \__ \ |_\__ \\
 |_|    |_|\__,_|\__, |_|_|___/\__|___/
                  __/ |                
                 |___/                 """.splitlines()
    gui += title
    gui.append('<centre>')
    gui.append('')
    gui.append('- SELECT SONGS -')

    for index, song in enumerate(data.song_library):
        bind_input(str(index + 3), make_playlist_lambda(index))
        gui.append(f"{index + 3}. {str(song)}" + (" (SELECTED)" if song in data.current_building_playlist.list_of_songs else ""))
        gui.append(' ')

    
    gui.append('<centre>')

    draw_gui_aligned(gui, 5)

    bind_input('2', lambda : data.set_state("PLAYLIST"))
    bind_input('1', lambda : create_playlist_and_switch())

    parse_input()

def state_generate_playlist ():
    reset_input_binds()

    if data.current_building_playlist == None:
        data.current_building_playlist = Playlist(input("Enter playlist name > "))
    
    gui = """  _____  _             _ _     _       
 |  __ \| |           | (_)   | |      
 | |__) | | __ _ _   _| |_ ___| |_ ___ 
 |  ___/| |/ _` | | | | | / __| __/ __|
 | |    | | (_| | |_| | | \__ \ |_\__ \\
 |_|    |_|\__,_|\__, |_|_|___/\__|___/
                  __/ |                
                 |___/                 """.splitlines()
    gui.append('<centre>')
    
    # get maximum time
    max_time_gui = [" "]
    max_time_gui.append('Enter the maximum allowed time in seconds (enter \'any\' for an unlimited time duration): ')
    max_time_gui.append('<centre>')

    draw_gui_aligned(gui + max_time_gui, 5)
    max_time_input = input("> ")

    if max_time_input.lower() == 'any':
        max_time = float('inf')
    else:
        max_time = float(max_time_input)
    
    # get genre
    genre_gui = [" "]
    genre_gui.append('Enter a specific genre (enter \'any\' for any genre): ')
    genre_gui.append('<centre>')

    draw_gui_aligned(gui + genre_gui, 5)
    genre_input = input("> ")
    
    if genre_input.lower() == 'any':
        genre_checker = lambda x : True
    else:
        genre_checker = lambda x : x == genre_input
    
    # generate
    num_songs = 0
    time = 0

    random.shuffle(data.song_library)
    for song in data.song_library:
        if time + song.length >= max_time:
            break
            
        if not genre_checker(song.genre):
            continue

        if genre_input.lower() != 'any' and num_songs >= 5:
            break

        time += song.length
        num_songs += 1
        data.current_building_playlist.add_song(song)
    
    data.song_library.sort(key=lambda song : ord(song.title[0]))
    
    create_playlist_and_switch()

#region EDIT DETAILS
def edit_favourite_artist ():
    data.current_user.fav_artist = input('Enter new favourite artist > ')
    data.current_user.serialise()

def edit_favourite_genre ():
    data.current_user.fav_genre = input('Enter favourite genre > ')
    data.current_user.serialise()

def delete_account ():
    data.current_user.delete()
    data.log_out()
    data.set_state('TITLE')

def state_edit_details ():
    reset_input_binds()

    gui = ["Type '1' to exit ..."]
    gui.append(' ')
    gui.append('<left>')
    gui += """  ______    _ _ _   
 |  ____|  | (_) |  
 | |__   __| |_| |_ 
 |  __| / _` | | __|
 | |___| (_| | | |_ 
 |______\__,_|_|\__|
                    
                    """.splitlines()
    gui.append('<centre>')
    gui.append(f'2. Edit favourite artist (currently {data.current_user.fav_artist})')
    gui.append('')
    gui.append(f'3. Edit favourite genre (currently {data.current_user.fav_genre})')
    gui.append('<centre>')
    gui.append('')
    gui.append('<!> 4. Delete account (IRREVERSIBLE)')
    gui.append('<centre>')

    draw_gui_aligned(gui, 5)

    bind_input('1', lambda : data.set_state('MAIN'))
    bind_input('2', lambda : edit_favourite_artist())
    bind_input('3', lambda : edit_favourite_genre())
    bind_input('4', lambda : delete_account())

    parse_input()
#endregion 

#region SONG LIBRARY
def save_artist_songs ():
    artist = input("Enter artist name > ")

    list_of_songs = []
    for song in data.song_library:
        if song.artist == artist:
            list_of_songs.append(song)
    
    file = open("output_log.txt", "wt")
    for song in list_of_songs:
        file.write(song.serialise() + "\n")
    file.close()

def genre_summary ():
    if not input("Enter creator password > ") == "OCRTUNES1234":
        print("INCORRECT PASSWORD")
        return
    
    genre_dict = {}
    for song in data.song_library:
        if not song.genre in genre_dict:
            genre_dict[song.genre] = [1, song.length]
        else:
            genre_dict[song.genre][0] += 1
            genre_dict[song.genre][1] += song.length
    
    for genre in genre_dict:
        print("Genre:", genre, ", Average Track Length (seconds):", genre_dict[genre][1] / genre_dict[genre][0])

def state_song_library ():
    reset_input_binds()

    gui = ["Type '1' to exit ..."]
    gui.append("Type '2' to save artist songs to a text file ...")
    gui.append("Type '3' to see summary of each genre ...")
    gui.append(' ')
    gui.append('<left>')
    gui += """   _____                       
  / ____|                      
 | (___   ___  _ __   __ _ ___ 
  \___ \ / _ \| '_ \ / _` / __|
  ____) | (_) | | | | (_| \__ \\
 |_____/ \___/|_| |_|\__, |___/
                      __/ |    
                     |___/     """.splitlines()
    gui.append('<centre>')
    gui.append(' ')

    for song in data.song_library:
        gui.append(str(song))
        gui.append(' ')
    
    gui.append('<centre>')

    draw_gui_aligned(gui, 5)

    bind_input('1', lambda : data.set_state('MAIN'))
    bind_input('2', lambda : save_artist_songs())
    bind_input('3', lambda : genre_summary())
    parse_input()
#endregion

while data.running:
    if data.state == 'TITLE':
        state_title()
    elif data.state == 'LOGIN':
        state_login()
    elif data.state == 'SIGNUP':
        state_signup()
    elif data.state == 'MAIN':
        state_main()
    elif data.state == 'SONGS':
        state_song_library()
    elif data.state == 'EDIT':
        state_edit_details()
    elif data.state == 'PLAYLIST':
        state_playlist_launchpad()
    elif data.state == 'PLAYLIST_CREATE':
        state_create_playlist()
    elif data.state == 'PLAYLIST_GENERATE':
        state_generate_playlist()
    else:
        print("INVALID STATE")
        data.exit()