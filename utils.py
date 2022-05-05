from tokenize import String
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import requests
import json
import random
import pylab as pl
from sympy import posify


def get_genre(term):
    url = "https://shazam.p.rapidapi.com/search"

    querystring = {"term":term,"locale":"en-US","offset":"0","limit":"5"}

    headers = {
	    "X-RapidAPI-Host": "shazam.p.rapidapi.com",
	    "X-RapidAPI-Key": "2108aba12emsh49279deedc868adp17c4d6jsn01373ba0c354"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)


    json_obj = json.loads(response.text)
    #print(json_obj)
    if("tracks" in json_obj):
        if ("track" in json_obj["tracks"]["hits"][0]):
            first_track = json_obj["tracks"]["hits"][0]["track"]
        else:
            return np.NaN
        key = first_track["key"]
    else: 
        return np.NaN
    url = "https://shazam.p.rapidapi.com/songs/get-details"



    querystring = {"key":key,"locale":"en-US"}

    headers = {
	    "X-RapidAPI-Host": "shazam.p.rapidapi.com",
	    "X-RapidAPI-Key": "2108aba12emsh49279deedc868adp17c4d6jsn01373ba0c354"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    json_str = response.text
    json_obj = json.loads(json_str)
    if("genres" in json_obj):
        results_genres = json_obj["genres"]
        return(results_genres["primary"])
    else:
        return np.NaN

def setup_genres(num):
    hist_df = pd.read_json("MyData/StreamingHistory0.json")
    lib_df = json.load(open("MyData/YourLibrary.json", "r", encoding="utf8"))
    lib_df = pd.DataFrame(lib_df["tracks"])

    hist_df_slice = hist_df.iloc[1:num].copy(deep=True)
    lib_df_slice = lib_df.iloc[1:num].copy(deep=True)
    
    lib_terms =lib_df_slice["track"] + " " + lib_df_slice["artist"]
    hist_terms = hist_df_slice["trackName"] + " " + hist_df_slice["artistName"]

    lib_genres = []
    hist_genres = []

    for item in lib_terms:
        lib_genres.append(get_genre(item))
    
    for item in hist_terms:
        hist_genres.append(get_genre(item))
   
    lib_df_slice["genres"] = lib_genres
    hist_df_slice["genres"] = hist_genres

    return lib_df_slice, hist_df_slice


def gen_rand_walks(num):
    rand_walks = []
    for i in range(0, num):
        prob = [0.5, 0.5]
        positions = [0]
        rr = np.random.random(1000)
        downp = rr < prob[0]
        upp = rr > prob[0]

        for idownp, iupp in zip(downp, upp):
            down = idownp and positions[-1] > -10
            up = iupp and positions[-1] < 10
            positions.append(positions[-1] - down + up)
        
        plt.figure()
        plt.plot(positions)
        plt.savefig("rand_walk" + str(i) + ".png")
        rand_walks.append("rand_walk" + str(i) + ".png")
    return rand_walks

def rgb_to_gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray

def box_count(list):
    dimensions = []
    for item in list:
        image = rgb_to_gray(pl.imread(item))
        pixels = []
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if image[i,j] > 0: 
                    pixels.append((i, j))
        Lx = image.shape[0]
        Ly = image.shape[1]
        pixels = pl.array(pixels)
        scales = np.logspace(0.01, 1, num=10, endpoint=False, base=2)
        Ns = []
        for scale in scales:
            # computing the histogram
            H, edges=np.histogramdd(pixels, bins=(np.arange(0,Lx,scale),np.arange(0,Ly,scale)))
            Ns.append(np.sum(H>0))

    # linear fit, polynomial of degree 1
        coeffs=np.polyfit(np.log(scales), np.log(Ns), 1)

        dimensions.append(-coeffs[0])
    
    return dimensions

