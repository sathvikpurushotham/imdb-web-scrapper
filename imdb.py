import requests 
import pandas as pd 
from bs4 import BeautifulSoup 
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import keys
title= input("Enter the name of the series\t")

seasonno=None
imdbid=None
try:
    jsonobj=requests.get("https://www.omdbapi.com/?apikey="+keys.apikey+"&t="+title) #enter your omdb-api key instead of keys.apikey
    imdbid=jsonobj.json()['imdbID']
    if imdbid!=None:
        print("Result of Type- "+jsonobj.json()['Type']+" found with Title- "+ jsonobj.json()['Title'])
    while(1):
        seasonno=int(input("Enter the season number (1-"+jsonobj.json()['totalSeasons']+")\t"))
        if seasonno<=int(jsonobj.json()['totalSeasons']) and seasonno>0 or seasonno==-1:
            break
        else:
            print("Season out of range, there are a maximum of "+jsonobj.json()['totalSeasons']+" in "+jsonobj.json()['Title'])
except:
    print("Not found")
if imdbid!=None and seasonno!=None:
    try:
        htmldata = requests.get("https://www.imdb.com/title/"+imdbid+"/episodes/_ajax?season="+str(seasonno)) 
    except:
        print("Error")
    soup = BeautifulSoup(htmldata.text, 'html.parser') 
    data = soup.find_all(class_="ipl-rating-star small")
    y=[float(i.find(class_="ipl-rating-star__rating").getText()) for i in data ]
    x=[i for i in range(1,len(y)+1)]
    
    fig, ax = plt.subplots(1,1)
    fig.canvas.set_window_title(jsonobj.json()['Title']+"  "+"Season "+str(seasonno))
    ax.plot(x,y)
    for xy in zip(x, y):                                       
        ax.annotate('(%s)' % xy[1], xy=xy) 
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.set_ylim([0, 10.5])
    plt.xlabel('Episodes')
    plt.ylabel('IMDB rating')
    plt.show()
    

else:
    pass

