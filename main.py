import os
import shutil
from mutagen.easyid3 import EasyID3
import re

#gets metadata from music files
def get_metadata(file_path):
    try:
        audio = EasyID3(file_path)
        album = audio["album"][0] if "album" in audio else "Unknown Album"
        date = audio["date"][0] if "date" in audio else "Unknown Year"
        year_match = re.search(r'\d{4}', date)
        year = year_match.group() if year_match else "Unknown Year"
        print(f"Got metadata for {audio}")
        return album, year
    except Exception as e:
        print(f"Error getting metadata for {file_path}: {e}")
        return None, None

#replaces invalid characters with "_", so Windows accepts the text as a folder name
def clean_string(string):
    return re.sub(r'[<>:"/\\|?*]', '_', string)

#moves files to folders (&makes folders)
def organize_music(source_folder):
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".mp3"):  #searches for .mp3 files
                file_path = os.path.join(root, file)
                album, year = get_metadata(file_path)
                if album and year:
                    #cleans the folder name
                    album = clean_string(album)
                    year = clean_string(year)
                    destination_folder = os.path.join(source_folder, f"{album} ({year})") #makes the folder
                    if not os.path.exists(destination_folder):
                        os.makedirs(destination_folder)
                    shutil.move(file_path, destination_folder)

#folder where the unsorted music is
main_folder = "C:\\folder\\path\\here"

organize_music(main_folder)