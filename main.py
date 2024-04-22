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

        print(f"\nGot metadata for {audio["title"]}.")

        return artist, album, year
    except Exception as e:
        print(f"Error getting metadata for {file_path}: {e}")
        return None, None, None

#replaces invalid characters with "_", so Windows accepts the text as a folder name
def clean_string(string):
    return re.sub(r'[<>:"/\\|?*]', '_', string)

#moves files to folders (&makes folders)
def organize_music(source_folder):
    audio_formats = (".mp3", ".wav", ".ogg", ".flac", ".m4a")

    for root, files in os.walk(source_folder):
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

                    destination_folder = os.path.join(source_folder, f"{artist} - {album} - ({year})") #makes the folder

                    if not os.path.exists(destination_folder):
                        os.makedirs(destination_folder)

                    #moves music to relevant folder(s)
                    try:
                        shutil.move(file_path, destination_folder)
                        print(f"Successfully moved {file_path}\nto {destination_folder}.")
                    except Exception as e:
                        print(f"Error moving {file_path} to {destination_folder}: {e}.")

#folder where the unsorted music is
main_folder = "C:\\folder\\path\\here"

organize_music(main_folder)