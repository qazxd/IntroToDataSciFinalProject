from tokenize import String
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import requests
import json


def get_genre(term):
    url = "https://shazam.p.rapidapi.com/search"

    querystring = {"term":term,"locale":"en-US","offset":"0","limit":"5"}

    headers = {
	    "X-RapidAPI-Host": "shazam.p.rapidapi.com",
	    "X-RapidAPI-Key": "2108aba12emsh49279deedc868adp17c4d6jsn01373ba0c354"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)


    json_obj = json.loads(response.text)

    if ("track" in json_obj["tracks"]["hits"][0]):
        first_track = json_obj["tracks"]["hits"][0]["track"]
    else:
        return np.NaN
    key = first_track["key"]

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

