
from bs4 import BeautifulSoup
import requests
import urllib.request


def getFavoriteAuthors(userURL):
    
    favoriteAuthors = list()
    
    userPage = requests.get(userURL)
    
    userSoup = BeautifulSoup(userPage.text, 'html.parser')
    
    stuff = userSoup.find(id = "fa")
    for user in stuff.findAll('a'):
        favoriteAuthors.append(user['href'])

    return favoriteAuthors

