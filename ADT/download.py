import os, sys, re, requests, subprocess, tabulate
from evdev import uinput, ecodes as code
from subprocess import call
from time import sleep
from bs4 import BeautifulSoup


class Download_Torrent():
    def __init__(self):

        p = 1

    def connection(self, url):

        try:
            connection = requests.get(url)
        except requests.RequestException as e:
            print (e)
            raise SystemExit('\n' + str(e))

        soup = BeautifulSoup(connection.content, 'html5lib')
        return soup

    def download_torrent(self, url):
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
                # self.search_begins()
        elif sys.platform.startswith('darwin'):
            call(['open', url])
        else:
            os.startfile(url)

    def search_begins_kat(self, name, boolean):
        print 'Search torrent on kickass \n'

        temp_url = 'https://kat.cr/usearch/'
        url_sort = '/?field=seeders&sorder=desc'

        print 'Searching...'
        url = temp_url + name + url_sort

        try:
            connection = requests.get(url)
        except requests.RequestException as e:
            raise SystemExit('\n' + str(e))

        if not re.findall(r'Download torrent file', str(connection.content), re.IGNORECASE):
            print('Torrents found: 0')
            self.search_begins_pirate_bay(name, boolean)
        else:
            soup = BeautifulSoup(connection.content, 'html5lib')

        age_seeder_leecher = [search.get_text() for search in soup.find_all('td', {'class': 'center'})]
        href = [search.get('href') for search in soup.find_all('a', {'title': 'Torrent magnet link'})]
        size = [search.get_text() for search in soup.find_all('td', {'class': 'nobr'})]
        title = [search.get_text() for search in soup.find_all('a', {'class': 'cellMainLink'})]

        age = age_seeder_leecher[2::5]
        seeders = age_seeder_leecher[3::5]
        leechers = age_seeder_leecher[4::5]

        table = [[
                     str(index + 1), title[index], size[index], age[index], seeders[index], leechers[index]
                 ] for index in range(len(href))]

        if boolean is True:

            print('\n')
            print(tabulate.tabulate(table, headers=['No', 'Title', 'Size', 'Age', 'Seeders', 'Leechers']))

            if len(href) == 1:
                torrent = 1
            else:
                print(
                '\nSelect torrent: [ 1 - ' + str(len(href)) + ' ] or [ M ] to go back to main menu or [ Q ] to quit')

                torrent = input('Enter the torrent index : \n')

            if torrent == 'Q' or torrent == 'q':
                sys.exit(0)
            elif torrent == 'M' or torrent == 'm':
                self.search_begins_kat(name, boolean)
            else:
                if int(torrent) <= 0 or int(torrent) > len(href):
                    print('Use eyeglasses...')
                    self.search_begins_kat(name, boolean)

                else:
                    print('Downloading...  >> ' + title[int(torrent - 1)] + '.torrent')
                    self.download_torrent(href[int(torrent) - 1])

                    print 'Arigato....'

        else:

            if len(href) <= 0:
                print('Use eyeglasses...')
                self.search_begins_pirate_bay(name, boolean)

            else:
                self.download_torrent(href[0])

    def search_begins_pirate_bay(self, name, boolean):
        print 'Search torrent on pirate bay \n'

        temp_url = 'https://thepiratebay-proxylist.org/'

        url = temp_url
        print url

        soup = self.connection(url)

        table = soup.find('table', {'class': 'proxies'})
        rows = table.findAll('tr')
        column = rows[1].findAll('td')
        link = column[0].find('a').get('href')
        print link

        name = str(name).replace(' ', '+')

        search_url = '/s/?q='
        search_end_url = '&page=0&orderby=99'

        url = link + search_url + name + search_end_url
        print url

        soup = self.connection(url)

        age_seeder_leecher = [search.get_text() for search in soup.find_all('td', {'align': 'right'})]

        href = [search.get('href') for search in soup.find_all('a', {'class': 'detLink'})]

        size = [search.get_text() for search in soup.find_all('font', {'class': 'detDesc'})]

        title = [search.get_text() for search in soup.find_all('a', {'class': 'detLink'})]

        k = 0
        for i in size:

            i = re.search('Size(.+?),', i)
            if i:
                size[k] = i.group(1)
                k = k + 1

        seeders = age_seeder_leecher[0::2]

        leechers = age_seeder_leecher[1::2]

        table = [[
                     str(index + 1), title[index], size[index], seeders[index], leechers[index]
                 ] for index in range(len(href))]

        if boolean is True:

            print('\n')
            print(tabulate.tabulate(table, headers=['No', 'Title', 'Size', 'Seeders', 'Leechers']))

            if len(href) == 1:
                torrent = 1
            else:
                print(
                '\nSelect torrent: [ 1 - ' + str(len(href)) + ' ] or [ M ] to go back to main menu or [ Q ] to quit')

                torrent = input('Enter the torrent index : \n')

            if torrent == 'Q' or torrent == 'q':
                sys.exit(0)
            elif torrent == 'M' or torrent == 'm':
                self.search_begins_kat(name, boolean)
            else:
                if int(torrent) <= 0 or int(torrent) > len(href):
                    print('Use eyeglasses...')


                else:
                    print('Downloading...  >> ' + title[int(torrent - 1)] + '.torrent')
                    self.download_torrent(href[int(torrent) - 1])

                    print 'Arigato....'

        else:

            if len(href) <= 0:
                print('Use eyeglasses...')


            else:
                self.download_torrent(href[0])


if __name__ == '__main__':
    try:
        emp1 = Download_Torrent()
        emp1.search_begins_kat('sdfg', False)
    except Exception as e:
        print (str(e))
        print ('\n Let me tell you a secret \n I am Batman')