import os, sys, re, requests, subprocess,tabulate

from evdev import uinput, ecodes as code
from subprocess import call
from time import sleep
from bs4 import BeautifulSoup


def download_torrent(url):
    print 'Opening torrent...'
    if os.name == 'nt':
        os.startfile(url)
    elif os.uname()[0] == 'Linux':
        pipe = subprocess.Popen(['xdg-open', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sleep(4)
        try:
            with uinput.UInput() as ui:
                ui.write(code.EV_KEY, code.KEY_ENTER, 1)
                ui.syn()
        except:
            print 'sorry, the permision for /dev/uinput is not granted \n'
            print 'Please run the command : chmod +0666 /dev/uinput\n'
            print 'and try again...'
            search_begins()
    elif sys.platform.startswith('darwin'):
        call(['open', url])
    else:
        os.startfile(url)


def search_begins():
    print 'Search torrent on pirate bay \n'

    temp_url = 'https://thepiratebay-proxylist.org/'
    url_sort = '/0/99/0'


    url = temp_url
    print url

    try:
        connection = requests.get(url)
    except requests.RequestException as e:
        print (e)
        raise SystemExit('\n' + str(e))

    soup = BeautifulSoup(connection.content, 'html5lib')

    table = soup.find('table', {'class': 'proxies'})
    rows = table.findAll('tr')
    column = rows[1].findAll('td')
    link = column[0].find('a').get('href')
    print link

    query = raw_input('Enter the torrent to be searched : ')
    query = query.replace(' ', '%20')
    print 'Searching...'

    query = str(query).replace(' ', '+')

    search_url = '/s/?q='
    search_end_url = '&page=0&orderby=99'

    url = link + search_url + query + search_end_url
    print url

    try:
        connection = requests.get(url)
    except requests.RequestException as e:
        print (e)
        raise SystemExit('\n' + str(e))



    soup = BeautifulSoup(connection.content, 'html5lib')


    age_seeder_leecher = [search.get_text() for search in soup.find_all('td', {'align': 'right'})]

    href = [search.get('href') for search in soup.find_all('a', {'class': 'detLink'})]

    size = [search.get_text() for search in soup.find_all('font', {'class': 'detDesc'})]

    title = [search.get_text() for search in soup.find_all('a', {'class': 'detLink'})]



    seeders = age_seeder_leecher[0::2]

    leechers = age_seeder_leecher[1::2]


    table = [[
                 str(index + 1), title[index], size[index],  seeders[index], leechers[index]
             ] for index in range(len(href))]

    print('\n')
    print(tabulate.tabulate(table, headers=['No', 'Title', 'Size', 'Seeders', 'Leechers']))

    if len(href) == 1:
        torrent = 1
    else:
        print('\nSelect torrent: [ 1 - ' + str(len(href)) + ' ] or [ M ] to go back to main menu or [ Q ] to quit')

        torrent = input('Enter the torrent index : \n')

    if torrent == 'Q' or torrent == 'q':
        sys.exit(0)
    elif torrent == 'M' or torrent == 'm':
        search_begins()
    else:
        if int(torrent) <= 0 or int(torrent) > len(href):
            print('Use eyeglasses...')
        else:
            print('Downloading...  >> ' + title[int(torrent - 1)] + '.torrent')
            download_torrent(href[int(torrent) - 1])

            print 'Arigato....'


if __name__ == '__main__':
    try:
        search_begins()
    except Exception as e:
        print (str(e))
        print ('\n Let me tell you a secret \n I am Batman')