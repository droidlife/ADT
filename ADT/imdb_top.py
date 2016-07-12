from bs4 import BeautifulSoup
import re
import os, sys, re, requests, subprocess, tabulate


class IMDB():
    def __init__(self):
        self.title = None

        self.base_url = 'http://www.imdb.com'

    def connection(self, url):

        try:
            connection = requests.get(url)
        except requests.RequestException as e:
            print (e)
            raise SystemExit('\n' + str(e))

        soup = BeautifulSoup(connection.content, 'html5lib')
        return soup

    def top_items(self, type):

        if type is "movie":

            extended_url = "/chart/top"
            url = self.base_url + extended_url
            print url

            soup = self.connection(url)

            top_movies = [search.get_text() for search in soup.find_all('td', {'class': 'titleColumn'})]

            imdb_rating = [search.get_text() for search in soup.find_all('td', {'class': 'ratingColumn imdbRating'})]

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
            top = top_movies
            imdb = imdb_rating





        elif type is "anime":
            extended_url = "/list/ls058654847/"
            url = self.base_url + extended_url
            print url

            soup = self.connection(url)
            top_animes = [search.get_text() for search in soup.find_all('div', {'class': 'list detail'})]
            print top_animes




        elif type is "shows":
            extended_url = "/chart/toptv/"
            url = self.base_url + extended_url
            print url

            soup = self.connection(url)
            print url

            top_shows = [search.get_text() for search in soup.find_all('td', {'class': 'titleColumn'})]

            imdb_rating = [search.get_text() for search in soup.find_all('td', {'class': 'ratingColumn imdbRating'})]

            k = 0
            for i in imdb_rating:
                imdb_rating[k] = i.strip()

                k = k + 1
            k = 0
            for i in top_shows:
                i = filter(lambda x: not x.isdigit(), i)
                i = i.strip()
                i = i.splitlines()
                top_shows[k] = i[1]
                top_shows[k] = top_shows[k].strip()
                print top_shows[k], imdb_rating[k]
                k = k + 1
            top = top_shows
            imdb = imdb_rating
        else:
            extended_url = ""

        table = [[
                     str(index + 1), top[index], imdb[index]
                 ] for index in range(len(top))]
        print('\n')
        print(tabulate.tabulate(table, headers=['No', 'Title', 'Rating']))


if __name__ == '__main__':
    try:
        emp1 = IMDB()
        emp1.top_items(type="movie")
    # emp1.hashtag()
    except Exception as e:
        print (str(e))
        print ('\n Let me tell you a secret \n I am Batman')

