import os
import sys
import subprocess


def create_folder_noexist_music():
    # can improve asking for a path to save to
    folder_name = input("Folder will be created in C:\\Users\\user\\Music, please name: ") #what if they don't write a folder at all?
    music_dir = os.path.expandvars(r'%USERPROFILE%\Music')
    folder_path = os.path.join(music_dir, folder_name)
    try:
        os.makedirs(folder_path)
        print(f"Folder '{folder_name}' created at: {folder_path}\n")
    except FileExistsError:
        print(f"'{folder_name}' already exists at: {folder_path}\n")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return folder_path

def create_folder_noexist_videos():
    folder_name = input("Folder will be created in C:\\Users\\user\\Videos, please name: ")
    video_dir = os.path.expandvars(r'%USERPROFILE%\Videos')
    folder_path = os.path.join(video_dir, folder_name)
    try:
        os.makedirs(folder_path)
        print(f"Folder '{folder_name}' created at: {folder_path}\n")
    except FileExistsError:
        print(f"'{folder_name}' already exists at: {folder_path}\n")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return folder_path

def talk_to_user():
    print("Choose on of the following options 1-5: \n")
    print(
    "1 - Single audio url\n"
    "2 - Custom list (from txt file) - audio\n"
    "3 - Youtube Playlist - audio\n"
    "4 - Single video url\n"
    "5 - Custome format video url (merges vid/aud streams)"
    )
    _choice = int(input("\nChoose an option: "))
    return _choice

def run_the_option(_choice):
    match _choice:
                # single url music
        case 1:
            _url = input("\nEnter URL: ")
            _format = input("Choose format (mp3, wav, etc): ")
            folder_path = create_folder_noexist_music()
            subprocess.run([
                "yt-dlp.exe",
                "-x",
                "--audio-format", _format,
                "-o", f"{folder_path}\\%(title)s.%(ext)s",
                _url
            ])
        
                # url/s from custom txt list - audio
        case 2:
            _txt_path = input("Enter txt file path: ").strip('"')
            _format = input("Choose format (mp3, wav etc)")
            folder_path = create_folder_noexist_music()
            subprocess.run([
                "yt-dlp.exe",
                "-x",
                "--audio-format", _format,
                "-o", f"{folder_path}\\%(title)s.%(ext)s",
                "-a", _txt_path
            ])
            
                # playlist from youtube link, has to be the link with the whole video list - audio
        case 3:
            _playlist_url = input("Enter playlist url (playlist link will have all the videos numbered): ")
            _format = input("Choose format (mp3, wav, etc): ")
            folder_path = create_folder_noexist_music()
            subprocess.run([
                "yt-dlp.exe",
                "-x",
                "--audio-format", _format,
                "-o", f"{folder_path}\\%(title)s.%(ext)s",
                "--yes-playlist", _playlist_url
            ])
            
                # single link - video
        case 4:
            _url = input("Enter URL: ")
            _format = input("Choose format (mp4, mov, etc): ")
            folder_path = create_folder_noexist_videos()
            subprocess.run([
                "yt-dlp.exe",
                "--merge-output-format", _format,
                "-o", f"{folder_path}\\%(title)s.%(ext)s",
                _url    
            ])
            
                # single link custom streams using -f, two numbers from list aud+vid will merge
        case 5:
            _url = input("Enter URL: ")
            print(_url)
            subprocess.run([
                "yt-dlp.exe",
                "--list-formats",
                "--no-playlist",
                _url
            ])
            _audio_format = input("Choose audio format: ")
            _video_format = input("Chose video format: ")
            folder_path = create_folder_noexist_videos()
            subprocess.run([
                "yt-dlp.exe",
                "-f", f"{_audio_format}+{_video_format}",
                "--no-playlist",
                "-o", f"{folder_path}\\%(title)s.%(ext)s",
                _url
            ])
                #input does not match case
        case _:
            print("You have not selected 1-5")


_choice = talk_to_user()
#_choice = choice
#print(f"\nChoice: {_choice}")
run_the_option(_choice)

while True:
    _continue = input("\nChoose again? y/n: ").lower()

    if _continue == 'y':
        _choice = talk_to_user()
        run_the_option(_choice)
    elif _continue == 'n':
        sys.exit(0)
