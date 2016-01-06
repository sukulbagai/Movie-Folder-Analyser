import requests
import os
import re
import json
import pickle
import sys

from Tkinter import Tk
from tkFileDialog import askdirectory


class Movie:
    movie_title=""
    year=""
    rated=""
    runtime=""
    genre=""
    director=""
    actors=""
    plot=""
    language=""
    rating=""

    def __init__(self,movie_title,year,rated,runtime,genre,director,actors,plot,language,rating):
        self.movie_title=movie_title
        self.year=year
        self.rated=rated
        self.runtime=runtime
        self.genre=genre
        self.director=director
        self.actors=actors
        self.plot=plot
        self.language=language
        self.rating=rating

def connected_to_internet(url='http://www.google.com/', timeout=3):
    try:
        temp = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:   
       return False

def data_exists(mypath):
    mypath+="/moviefolderinfo.dat"
    return os.path.exists(mypath)

# Function to rename the file to a proper movie name
def correct_name(str):
  names_list=["\\[.*\\]","\\(.*\\)","720p","1080p","x264","[1|2][9|0]\\d{2}","dvd\\.?rip","xvid","VPPV",
              "CD\\d+","-axxo","mp3","hdtv","divx","sharkboy","\\d{0,2}fps","\\d{0,3}kbps","hddvd",
              "torr?ent.","extended","WunSeeDee","\\d{3,4}p","Part\\d","-","YIFY","x264","BluRay",
              "mp4","avi","mkv","m4v","flv","vob","mpg","SPARKS","mpeg","BrRip","\\.\\.+","BRRip","AACETRG"]
  for temp in names_list:
    str=str.replace(temp,"")
    str=re.sub(temp,"",str)
  str=str.strip()
  str=str.replace("."," ")
  return str


# Function that send movie name as a paremeter and retrieves and
# displays data by using the movie name as a search string
def get_online_results(search_parameter,mypath):
    api_url = "http://www.omdbapi.com"
    params = {
        "t": search_parameter,
        "plot": "short",
        "r": "json",
        "type": "movie"
    }
    response = requests.get(api_url, params=params)
    #print("json:\n%s" % response, json.dumps(response.json(), indent=4))
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
    rating = response_data.get("imdbRating", "")

    movieObject = Movie(movie_title,year,rated,runtime,genre,director,actors,plot,language,rating)
    mypath+="/moviefolderinfo.dat"
    movieDataFile = open(mypath,"ab")
    pickle.dump(movieObject,movieDataFile)
    movieDataFile.close()

    printing_string= movie_title+"\n"+year+"\n"+rated+"\n"+runtime+"\n"+genre+"\n"+director+"\n"+actors+"\n"+plot+"\n"+language+"\n"+rating
    #print movie_title, "\n", year, "\n", rated, "\n", runtime, "\n", genre, "\n", director, "\n", actors, "\n", plot, "\n", language, "\n", rating
    print printing_string.encode('ascii','ignore')


def get_offline_results(search_parameter,mypath):
    mypath+="/moviefolderinfo.dat"
    movieDataFile = open(mypath,"rb")
    while(1):
        try:
            movieObject = pickle.load(movieDataFile)
            if(movieObject.movie_title==search_parameter):
                printing_string= movieObject.movie_title+"\n"+movieObject.year+"\n"+movieObject.rated+"\n"+movieObject.runtime+"\n"+movieObject.genre+"\n"+movieObject.director+"\n"+movieObject.actors+"\n"+movieObject.plot+"\n"+movieObject.language+"\n"+movieObject.rating
                print printing_string.encode('ascii','ignore')
                break
        except EOFError:
            print "Offline Record Not Found."
            break
    movieDataFile.close()



if __name__ == "__main__":
    Tk().withdraw()
    mypath = askdirectory()

    if(not connected_to_internet() and not data_exists(mypath)):
        print "No Connection and Offline Data Unavailable. Sorry."
        sys.exit()
    if(connected_to_internet() and data_exists(mypath)):
        os.remove(mypath+"/moviefolderinfo.dat")

    format_list=[".mov",".avi",".mpg",".mpeg",".mp4",".vob",".flv",".mkv",".m4v"]
    for r,d,f in os.walk(mypath):
        
        for files in f:
            correct_format=False
            for formats in format_list:
                if(files.endswith(formats)):
                    correct_format=True
                    break
            
            if(correct_format):
                if(connected_to_internet()):
                    get_online_results(correct_name(files),mypath)
                    print("\n\n" + "-" * 30 + "\n\n")
                else:
                    print "Lost Connection to Internet."
                    if(data_exists(mypath)):
                        print "Trying to Fetch Data from Previous Execution.\n"
                        get_offline_results(correct_name(files),mypath)
                        print("\n\n" + "-" * 30 + "\n\n")
