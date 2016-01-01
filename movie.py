import requests
import os
import re
import json

from Tkinter import Tk
from tkFileDialog import askdirectory


# Function to rename the file to a proper movie name
def correct_name(raw_name):
    names_to_strip = ["\\[.*\\]", "\\(.*\\)", "720p", "1080p", "x264",
                      "[1|2][9|0]\\d{2}", "dvd\\.?rip", "xvid",
                      "CD\\d+", "-axxo", "mp3", "hdtv", "divx",
                      "sharkboy", "\\d{0,2}fps", "\\d{0,3}kbps",
                      "hddvd", "torr?ent.", "extended", "WunSeeDee",
                      "\\d{3,4}p", "Part\\d", "-", "YIFY", "x264",
                      "BluRay", "mp4", "avi", "mkv", "m4v", "flv",
                      "vob", "mpg", "SPARKS", "mpeg", "BrRip", "\\.\\.+",
                      "BRRip", "AACETRG"]
    for name in names_to_strip:
        corrected_name = raw_name.replace(name, "")
        corrected_name = re.sub(name, "", corrected_name)

    corrected_name = corrected_name.strip()
    corrected_name = corrected_name.replace(".", " ")

    return corrected_name


# Function that send movie name as a paremeter and retrieves and
# displays data by using the movie name as a search string
def get_results(search_parameter):
    api_url = "http://www.omdbapi.com"
    params = {
        "t": search_parameter,
        "plot": "short",
        "r": "json",
        "type": "movie"
    }
    response = requests.get(api_url, params=params)
    print("json:\n%s" % response, json.dumps(response.json(), indent=4))
    response_data = response.json()

    if response_data["Response"] == "False":
        return None

    movie_title = response_data.get("Title", "")
    year = response_data.get("Year", "")
    rated = response_data.get("Rated", "")
    runtime = response_data.get("Runtime", "")
    genre = response_data.get("Genre", "")
    director = response_data.get("Director", "")
    actors = response_data.get("Actors", "")
    plot = response_data.get("Plot", "")
    language = response_data.get("Language", "")
    rating = response_data.get("Rating", "")

    print(movie_title, "\n", year, "\n", rated, "\n", runtime, "\n",
          genre, "\n", director, "\n", actors, "\n", plot, "\n",
          language, "\n", rating)


if __name__ == "__main__":
    Tk().withdraw()
    mypath = askdirectory()

    movie_files = os.listdir(mypath)

    for files in movie_files:
        get_results(correct_name(files))
        print("\n\n" + "-" * 30 + "\n\n")
