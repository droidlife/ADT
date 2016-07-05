import requests
from bs4 import BeautifulSoup


class IMDB:
    def __init__(self):
        self.title = None

        self.base_url = 'http://www.imdb.com'
        self.search_url = '/find?q='
        self.episode_list_url = 'episodes?ref_=tt_ov_epl'

        self.age = None
        self.title_header = None
        self.season = None

    def search_title(self):
        search_title = str(self.title).replace(' ', '+')
        url = self.base_url + self.search_url + search_title
        try:
            connection = requests.get(url)
        except requests.RequestException as e:
            raise SystemExit('\n' + str(e))

        soup = BeautifulSoup(connection.content, 'html5lib')

        table = soup.find('table', {'class': 'findList'})
        rows = table.findAll('tr')
        column = rows[0].findAll('td')
        link = column[1].find('a').get('href')
        connection.close()

        return link

    def parse_link_to_episodes_link(self, link):
        links = str(link).split('?')
        link = links[0] + 'episodes?ref_=tt_ov_epl'
        url = self.base_url + link

        return url

    def get_episode_details(self, url):
        try:
            connection = requests.get(url)
        except requests.RequestException as e:
            raise SystemExit('\n' + str(e))

        soup = BeautifulSoup(connection.content, 'html5lib')
        information = soup.find_all('div', {'class': 'info'})
        age = soup.find_all('div', {'class': 'airdate'})
        link = information[-1].find('a')['href']
        self.title_header = information[-1].find('a')['title']
        self.age = str(age[-1].get_text()).strip()

        connection.close()

        url = self.base_url + link

        self.season = self._get_episode_number(url=url)

    def _get_episode_number(self, url):
        try:
            connection = requests.get(url)
        except requests.RequestException as e:
            raise SystemExit('\n' + str(e))

        soup = BeautifulSoup(connection.content, 'html5lib')
        seasons = soup.find_all('div', {'class': 'bp_heading'})

        connection.close()
        return seasons[0].get_text()

    def get_latest_episode(self, title):
        self.title = title
        link = self.search_title()
        episode_link = self.parse_link_to_episodes_link(link=link)
        self.get_episode_details(url=episode_link)

        return self.title_header, self.season, self.age

    def get_next_episode(self, title):
        search_title = str(title).replace(' ', '-')
        url = 'https://www.episodate.com/tv-show/' + search_title
        try:
            connection = requests.get(url)
        except requests.RequestException as e:
            raise SystemExit('\n' + str(e))

        soup = BeautifulSoup(connection.content, 'html5lib')
        next_episode = soup.find_all('div', {'class': 'col-md-6'})
        if next_episode[1].find('b', {'class': 'color-green'}):
            details = next_episode[1].find('b', {'class': 'color-green'})
            date = next_episode[1].find('b', {'class': 'episode_datetime_convert'})
            return details.get_text(), date.get_text()
        else:
            return None,None
