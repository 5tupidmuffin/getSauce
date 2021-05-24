"""
Web Scrapping Script to extract information from external sites
"""
from bs4 import BeautifulSoup
from getSauce import logit
import re
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0', 
'referer': None
}


# created classes for ease of data access
class movieInformation:
    def __init__(self, title, releaseDate, genre, runtime, rating, trailerLink, posterLink, description, streaminglink, sourcelink):
        self.title = title
        self.releaseDate = releaseDate
        self.genre = genre
        self.runtime = runtime
        self.rating = rating
        self.poster = posterLink
        self.trailer = trailerLink
        self.description = description
        self.sourcelink = sourcelink
        self.stream = streaminglink


class animeInformation:
    def __init__(self, title, releasedate, rating, runtime, posterlink, streaminglink, genre, typeofmedia, description, sourcelink):
        self.title = title
        self.releaseDate = releasedate
        self.type_of_anime = typeofmedia
        self.rating = rating
        self.runtime = runtime
        self.genre = genre
        self.poster = posterlink
        self.stream = streaminglink
        self.description = description
        self.sourcelink = sourcelink



def getVideoInfo(url_to_imdb):
    """
    Retrieves Information about Media From IMDB
    
    url_to_imdb : IMDB url to the media
    """
    htmlcontent = requests.get(url_to_imdb, headers=headers).text  # using header to extract trailer link
    soup = BeautifulSoup(htmlcontent, 'lxml')

    information = soup.find('div', class_ = 'title_wrapper')

    streaminglink = None
    steaminglinkblock = soup.find('div', class_ = re.compile("^buybox"))

    if steaminglinkblock:
        streaminglink = 'https://imdb.com' + steaminglinkblock.find('a').get('href')

    title = information.find('h1', class_ = '').text
    releasedate = information.find('a', title = 'See more release dates').text.strip()
    runtime = information.find('time').text.strip()
    imdb_rating = float(soup.find('span', itemprop= 'ratingValue').text)

    trailer_link = 'https://www.imdb.com' + soup.find('a', class_ = 'slate_button prevent-ad-overlay video-modal').get('href')

    poster_block = BeautifulSoup(htmlcontent, 'lxml').find('div', class_ = 'poster')
    poster_link = poster_block.find('img').get('src')

    description = soup.find('div', class_ = 'summary_text').text

    raw_gernes = information.find_all('a')
    genres = []
    for genre in raw_gernes:
        genres.append(genre.text)

    genres.pop()  # pop the last item which is the release date
    genres.pop(0)  # pop first item which is the release year
    logit("******** Info Successfully Fetched From IMDB ********")
    return movieInformation(title, releasedate, genres, runtime, imdb_rating, trailer_link, poster_link, description, streaminglink, url_to_imdb)


# anidb link = https://anidb.net/anime/12986      devilman crybaby
def getAnimeInfo(url_to_anidb):
    """
    Retrieves Information about media from ANIDB

    url_to_anidb : ANIDB url for media
    """
    htmlcontent = requests.get(url_to_anidb, headers= headers).text
    soup = BeautifulSoup(htmlcontent, 'lxml')
    information = soup.find('div', class_='g_section info')

    # print(information.prettify())

    title = information.find('span', itemprop='name').text.strip()
    releasedate = information.find('tr', class_ = 'year').text.replace('Year', '').strip()
    rating = float(information.find('span', itemprop='ratingValue').text.strip())
    runtime = soup.find('div', class_ = 'g_bubble duration').text.replace('Running Time', '').strip()

    poster_link = information.find('img', class_ = 'g_image g_bubble').get('src')
    poster_link = poster_link.replace('https', 'http')  # to solve the anidb poster fetch problem requires app to run on https

    streaming_link = information.find('a', title= "Official stream")
    if streaming_link:
        streaming_link = streaming_link.get('href')


    description = soup.find('div', itemprop= 'description').text.strip()
    type_of_anime = information.find('tr', class_ = re.compile('.*type.*')).text.replace('Type', '').strip()

    raw_genres = information.find_all('span', class_ = 'tagname')
    genres = []
    for genre in raw_genres:
        genres.append(genre.text.strip())

    logit("******** Info Successfully Fetched From Anidb ********")
    return animeInformation(title, releasedate, rating, runtime, poster_link, streaming_link, genres, type_of_anime, description, url_to_anidb)
