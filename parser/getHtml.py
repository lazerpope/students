import requests

url = 'https://darling-in-the-franxx.fandom.com/wiki/Hiro'


itemsJson = []

def getHtml(url):
    r = requests.get(url)
    return r.text


with open('index.html','w',encoding='utf-8') as f:
    f.write(getHtml(url))
