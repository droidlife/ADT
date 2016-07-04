import re, os, sys
from imdb import IMDB


class Command:
    def __init__(self):
        self.file_path = None

    def search_query(self):
        query = raw_input('\nEnter the torrent to be searched : \t').strip().lower()

        if re.match(r'quit\b', query, flags=re.IGNORECASE):
            sys.exit(0)

        elif re.match(r'search\b', query, flags=re.IGNORECASE):
            print 'searching for torrent'

        elif re.match(r'add\b', query, flags=re.IGNORECASE):
            title_head = query[4:].strip()

            title_exist = False
            if os.path.isfile(os.path.expanduser(self.file_path)):
                file = open(os.path.expanduser(self.file_path), 'r')
                lines = file.readlines()
                file.close()
                for line in lines:
                    if line.__contains__(title_head):
                        title_exist = True
                if title_exist:
                    print '\n' + 'You already follow ' + title_head.upper()
                else:
                    file = open(os.path.expanduser(self.file_path), 'a')
                    season, age = IMDB().get_next_episode(title=title_head)
                    data = title_head + '/' + season + '/' + age
                    file.write(data + '\n')
                    file.close()
                    print '\n' + title_head.upper() + ' has been added.'
                    print '\n' + 'New torrent will be downloaded automatically.'
                    print 'The new episode will air on ' + age

            else:
                file = open(os.path.expanduser(self.file_path), 'a')
                season, age = IMDB().get_next_episode(title=title_head)
                data = title_head + '/' + season + '/' + age
                file.write(data + '\n')
                file.close()
                print '\n' + title_head.upper() + ' has been added.'
                print '\n' + 'New torrent will be downloaded automatically.'
                print 'The new episode will air on ' + age

            self.search_query()

    def search(self):
        self._get_file_path()
        try:
            self.search_query()
        except:
            print 'Goodbye...'

    def _get_file_path(self):
        if os.name == 'nt':
            pass
        elif os.uname()[0] == 'Linux':
            self.file_path = '~/.follow'
        elif sys.platform.startswith('darwin'):
            self.file_path = '~/.follow'
