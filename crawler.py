#!/usr/local/bin/python3

import http
import http.client
import sys
import os
import pyquery
from urllib import parse
import requests

def download(url, filename, dir):
    print("Downloading " + url + " into " + dir + "/" + filename)
    if not os.path.exists(dir):
        os.makedirs(dir)
    img = requests.get(url).content
    with open(dir+'/'+filename, 'wb') as handler:
        handler.write(img)
    return

if len(sys.argv) < 2:
    print("Too few arguments")
    sys.exit()

url = sys.argv[1]

targetURL = parse.urlparse(url)
print("Crawling " + targetURL.path + " from " + targetURL.netloc)

connection = http.client.HTTPSConnection(targetURL.netloc)
connection.request('GET', targetURL.path)
response = connection.getresponse()


pq = pyquery.PyQuery(response.read().decode())
title = pq('h1.productinfo__h').text().translate(str.maketrans({"-":  r"_",
                                          "]":  r"_",
                                          "\\": r"_",
                                          "^":  r"_",
                                          "$":  r"_",
                                          "*":  r"_",
                                          "\"": r"_",
                                          "\'": r"_",
                                          " ":  r"_",
                                          ":":  r"_",
                                          ".":  r"_"}))
print("Item title: " + title)
items = pq('img.productphoto__photo')

for item in items.items():
    img = item.attr['data-highres']
    parts = img.split('/')
    filename = parts[len(parts)-1]
    fullURL = "https://"+targetURL.netloc+img
    download(fullURL, filename, title)
    #parts = parse.urlparse(img)


    #print("==================\n"+pq(item).html()+"\n=============================\n")