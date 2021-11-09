import flask
import os
from dotenv import find_dotenv, load_dotenv
import requests
import base64
import hashlib
import time

# https://stackoverflow.com/questions/53356636/invalid-hash-timestamp-and-key-combination-in-marvel-api-call helped me get the api calls to work

load_dotenv(find_dotenv())

public_key = os.getenv("marvel_public_key")
private_key = os.getenv("marvel_private_key")

hash = hashlib.md5()

base_url = "https://gateway.marvel.com/v1/public/comics"

# The Marvel API requires servers to have parameters before accessing them. The paramaters are: a timestamp (ts), the public api key, and a hash with the md5 algorithm of the ts, public key, and private key mashed together
# To do this, I made ts a random time, converted ts, public key, and private key into byte format so they can be fed into the md5 formatter, and then convert the hashed string into the hex form, which is the form required by the Marvel API.
ts = "randomtime"
ts_byte = bytes(ts, "utf-8")
public_byte = bytes(public_key, "utf-8")
private_byte = bytes(private_key, "utf-8")
hash.update(ts_byte)
hash.update(private_byte)
hash.update(public_byte)
hashhex = hash.hexdigest()

search = input("Enter the title of the comic you would like to search for ")


def getComicByTitle(search):
    params = {
        "ts": ts,
        "apikey": public_key,
        "hash": hashhex,
        "title": search,
        "limit": 1,
    }
    endpoint_request = requests.get(url=base_url, params=params)
    data = endpoint_request.json()
    data_results = data["data"]["results"]
    title = data_results[0]["title"]
    creators = data_results[0]["creators"]["items"]
    dates = data_results[0]["dates"][0]["date"]
    creatorList = []
    for i in range(len(creators)):
        creatorList.append(data_results[0]["creators"]["items"][i]["name"])
    urls = data_results[0]["urls"]

    print(f"{dates}")
    # print(data_results[0].keys())


getComicByTitle(search)
