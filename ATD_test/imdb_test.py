import requests
from bs4 import BeautifulSoup


def get_next_episode(title):
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

v,x= get_next_episode(title='game of thrones')
print v