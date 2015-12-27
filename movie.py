import requests
import os,sys
import re
from Tkinter import Tk
from tkFileDialog import askdirectory

#Function to rename the file to a proper movie name
def correct_name(str):
	names_list=["\\[.*\\]","\\(.*\\)","720p","1080p","x264","[1|2][9|0]\\d{2}","dvd\\.?rip","xvid","CD\\d+","-axxo","mp3","hdtv","divx","sharkboy","\\d{0,2}fps","\\d{0,3}kbps","hddvd","torr?ent.","extended","WunSeeDee","\\d{3,4}p","Part\\d","-","YIFY","x264","BluRay","mp4","avi","mkv","m4v","flv","vob","mpg","SPARKS","mpeg","BrRip","\\.\\.+","BRRip","AACETRG"]
	for temp in names_list:
		str=str.replace(temp,"")
		str=re.sub(temp,"",str)
	str=str.strip()
	str=str.replace("."," ")
	return str

#Function that send movie name as a paremeter and retrieves and displays data by using the movie name as a search string
def get_results(search_parameter):
	url='http://www.omdbapi.com/?t='
	url+=search_parameter
	url+='&plot=short&r=xml&type=movie'

	r=requests.get(url)
	data=r.text.encode('utf8')
	search_string="root response=\""
	pos=data.find(search_string)

	#Successful Search
	if(data[pos+len(search_string)]=='T'):

		#Movie Title
		search_string="movie title=\""
		pos=data.find(search_string)
		movie_title=""
		pos=pos+len(search_string)
		while(1):
			if(data[pos]=='\"'):
				break
			movie_title+=data[pos]
			pos+=1

		#Year
		search_string="year=\""
		pos=data.find(search_string)
		year=""
		pos=pos+len(search_string)
		while(1):
			if(data[pos]=='\"'):
				break
			year+=data[pos]
			pos+=1

		#Rated
		search_string="rated=\""
		pos=data.find(search_string)
		rated=""
		pos=pos+len(search_string)
		while(1):
			if(data[pos]=='\"'):
				break
			rated+=data[pos]
			pos+=1

		#Runtime
		search_string="runtime=\""
		pos=data.find(search_string)
		runtime=""
		pos=pos+len(search_string)
		while(1):
			if(data[pos]=='\"'):
				break
			runtime+=data[pos]
			pos+=1

		#Genre
		search_string="genre=\""
		pos=data.find(search_string)
		genre=""
		pos=pos+len(search_string)
		while(1):
			if(data[pos]=='\"'):
				break
			genre+=data[pos]
			pos+=1

		#Director
		search_string="director=\""
		pos=data.find(search_string)
		director=""
		pos=pos+len(search_string)
		while(1):
			if(data[pos]=='\"'):
				break
			director+=data[pos]
			pos+=1

		#Actors
		search_string="actors=\""
		pos=data.find(search_string)
		actors=""
		pos=pos+len(search_string)
		while(1):
			if(data[pos]=='\"'):
				break
			actors+=data[pos]
			pos+=1

		#Plot
		search_string="plot=\""
		pos=data.find(search_string)
		plot=""
		pos=pos+len(search_string)
		while(1):
			if(data[pos]=='\"'):
				break
			plot+=data[pos]
			pos+=1

		#Language
		search_string="language=\""
		pos=data.find(search_string)
		language=""
		pos=pos+len(search_string)
		while(1):
			if(data[pos]=='\"'):
				break
			language+=data[pos]
			pos+=1

		#Rating
		search_string="imdbRating=\""
		pos=data.find(search_string)
		rating=""
		pos=pos+len(search_string)
		while(1):
			if(data[pos]=='\"'):
				break
			rating+=data[pos]
			pos+=1


		#Printing All Retrieved Attributes
		print movie_title,"\n",year,"\n",rated,"\n",runtime,"\n",genre,"\n",director,"\n",actors,"\n",plot,"\n",language,"\n",rating

	#Unsuccessful Search
	else:
		print "No Data Found"

Tk().withdraw()
mypath=askdirectory()
onlyfiles = os.listdir(mypath)
for files in onlyfiles:
	get_results(correct_name(files))
	print "\n\n------------------------------------------------------\n\n"