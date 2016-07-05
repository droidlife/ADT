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
                    data = title_head + '/' + str(season) + '/' + str(age)
                    file.write(data + '\n')
                    file.close()
                    print '\n' + title_head.upper() + ' has been added.'
                    if age is not None:
                        print '\n The new episode will air on ' + age
                        print '\n' + 'New torrent will be downloaded automatically.'
                    else:
                        print '\n The new episode air date is not out yet.'
                        print '\n New torrent will be downloaded when the air date arrives.'

            else:
                file = open(os.path.expanduser(self.file_path), 'a')
                season, age = IMDB().get_next_episode(title=title_head)
                data = title_head + '/' + str(season) + '/' + str(age)
                file.write(data + '\n')
                file.close()
                print '\n' + title_head.upper() + ' has been added.'
                if age is not None:
                    print '\n The new episode will air on ' + age
                    print '\n' + 'New torrent will be downloaded automatically.'
                else:
                    print '\n The new episode air date is not out yet.'
                    print '\n New torrent will be downloaded when the air date arrives.'

            self.search_query()

        elif re.match(r'remove\b', query, flags=re.IGNORECASE):
            title_head = query[7:].strip()

            if os.path.isfile(os.path.expanduser(self.file_path)):
                file = open(os.path.expanduser(self.file_path), 'r')
                lines = file.readlines()
                file.close()
                file = open(os.path.expanduser(self.file_path), 'w')
                for line in lines:
                    if not line.__contains__(title_head):
                        file.write(line)
                file.write("\n")
                file.close()
                print 'Removed ' + title_head.upper()

            else:
                print '\n You are not following ' + title_head.upper()
                print '\n Use the commnad ADD <title> to start following'

            self.search_query()

    def search(self):
        self._get_file_path()
        try:
            self.search_query()
        except Exception as e:
            print str(e)
            print 'Goodbye...'

    def _get_file_path(self):
        if os.name == 'nt':
            pass
        elif os.uname()[0] == 'Linux':
            self.file_path = '~/.follow'
        elif sys.platform.startswith('darwin'):
            self.file_path = '~/.follow'
