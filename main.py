import os
import shutil
import re
from mutagen.easyid3 import EasyID3

#gets metadata from music files
def get_metadata(file_path):
    try:
        audio = EasyID3(file_path)

        #takes metadata from audio files
        artist = audio["artist"][0] if "artist" in audio else "Unknown Artist"
        album = audio["album"][0] if "album" in audio else "Unknown Album"
        date = audio["date"][0] if "date" in audio else "Unknown Year"

        #only uses the first (hopefully main) artist's name
        if "/" in artist:
            artist = artist.split("/")[0].strip()

        #converts complete date to album year only
        if date != "Unknown Year":
            year_match = re.search(r'\d{4}', date)
            year = year_match.group() if year_match else "Unknown Year"

        print(f"\nGot metadata for {audio['title']}.")

        return artist, album, year
    except Exception as e:
        print(f"Error getting metadata for {file_path}: {e}")
        return None, None, None

#replaces invalid characters with "_", so Windows accepts the text as a folder name
def clean_string(string):
    return re.sub(r'[<>:"/\\|?*]', '_', string)

#moves files to folders (&makes folders)
def organize_music(source_folder):
    album_folders = {}
    audio_formats = (".mp3", ".wav", ".ogg", ".flac", ".m4a")

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            #searches for .mp3 files
            if any(file.endswith(ext) for ext in audio_formats):
                file_path = os.path.join(root, file)
                artist, album, year = get_metadata(file_path)

                if artist and album and year:
                    #cleans the folder name
                    artist = clean_string(artist)
                    album = clean_string(album)
                    year = clean_string(year)

                    destination_folder = os.path.join(source_folder, f"{album} - {artist} ({year})") #makes the folder

                    # print(os.path.basename(destination_folder))
                    # if artist not in os.path.basename(destination_folder):
                    album_key = (album, year)
                    if album_key not in album_folders:
                        album_folders[album_key] = destination_folder
                        if not os.path.exists(destination_folder):
                            os.makedirs(destination_folder)

                    #moves music to relevant folder(s)
                    try:
                        shutil.move(file_path, album_folders[album_key])
                        print(f"Successfully moved {file_path}\nto folder {album_folders[album_key]}.")
                    except Exception as e:
                        print(f"Error moving {file_path}\nto folder {album_folders[album_key]}: {e}")

if __name__ == "__main__":
    print("------------------------------------")
    print("Welcome to the Music Sorter script!")
    print("------------------------------------")

    print("Leave the name blank for using current (script's location) folder.")
    print("Windows path example: C:\\Users\\User\\Music\\")
    print("Linux/MacOS path example: /home/username/music")
    
    main_folder = str(input("Enter the path to the folder containing the music you want to organize: "))
    if not main_folder:
        main_folder = os.getcwd()

    organize_music(main_folder)

    print("\n Script is finished.")
    print("Please report any issues on GitHub: https://github.com/vb2007/music-sorter")
