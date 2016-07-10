import requests
from bs4 import BeautifulSoup
import re


class IMDB:
    def __init__(self):
        self.title = None

        self.base_url = 'http://www.imdb.com'

    def top_items(self, type):

        print 'ss'

        if type is "movie":

            extended_url = "/chart/top"
            url = self.base_url + extended_url
            print url

            try:
                connection = requests.get(url)
            except requests.RequestException as e:
                print (e)
                raise SystemExit('\n' + str(e))

            soup = BeautifulSoup(connection.content, 'html5lib')
            print url

            top_movies = [search.get_text() for search in soup.find_all('td', {'class': 'titleColumn'})]

            imdb_rating = [search.get_text() for search in soup.find_all('td', {'class': 'ratingColumn imdbRating'})]
            print imdb_rating
            k = 0
            for i in imdb_rating:
                imdb_rating[k] = i.strip()
                k = k + 1
            k = 0
            for i in top_movies:
                i = filter(lambda x: not x.isdigit(), i)
                i = i.strip()
                i = i.splitlines()
                top_movies[k] = i[1]
                top_movies[k] = top_movies[k].strip()

                k = k + 1




        elif type is "anime":
            extended_url = "/list/ls058654847/"
            url = self.base_url + extended_url
            print url

            try:
                connection = requests.get(url)
            except requests.RequestException as e:
                print (e)
                raise SystemExit('\n' + str(e))

            soup = BeautifulSoup(connection.content, 'html5lib')
            print url
            top_animes = [search.get_text() for search in soup.find_all('div', {'class': 'list detail'})]
            print top_animes




        elif type is "shows":
            extended_url = "/chart/toptv/"
            url = self.base_url + extended_url
            print url

            try:
                connection = requests.get(url)
            except requests.RequestException as e:
                print (e)
                raise SystemExit('\n' + str(e))

            soup = BeautifulSoup(connection.content, 'html5lib')
            print url

            top_shows = [search.get_text() for search in soup.find_all('td', {'class': 'titleColumn'})]

            imdb_rating = [search.get_text() for search in soup.find_all('td', {'class': 'ratingColumn imdbRating'})]

            k = 0
            for i in imdb_rating:
                imdb_rating[k] = i.strip()
                print imdb_rating[k]
                k = k + 1
            k = 0
            for i in top_shows:
                i = filter(lambda x: not x.isdigit(), i)
                i = i.strip()
                i = i.splitlines()
                top_shows[k] = i[1]
                top_shows[k] = top_shows[k].strip()
                print top_shows[k]
                k = k + 1
        else:
            extended_url = ""



if __name__ == '__main__':
    try:
        emp1 = IMDB()
        emp1.top_items(type="movie")
    # emp1.hashtag()
    except Exception as e:
        print (str(e))
        print ('\n Let me tell you a secret \n I am Batman')

