import re, os, sys
from imdb import IMDB
from download import Download_Torrent
from imdb_top import IMDB_TOP


class Command:
    def __init__(self):
        self.file_path = None

    def search_query(self):
        query = raw_input('\nEnter the torrent to be searched : \t').strip().lower()

        if re.match(r'quit\b', query, flags=re.IGNORECASE):
            print '\nGoodbye...'
            sys.exit(0)

        elif re.match(r'search\b', query, flags=re.IGNORECASE):
            title_head = query[7:].strip()
            try:
                Download_Torrent().search_begins_kat(name=title_head, boolean=True)
                self.search_query()
            except:
                print '\nSorry torrent can not be downloaded.\nPlease Try again'
                self.search_query()

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
                        print '\nThe new episode will air on ' + age
                        print '\n' + 'New torrent will be downloaded automatically.'
                    else:
                        print '\nThe new episode air date is not out yet.'
                        print '\nNew torrent will be downloaded when the air date arrives.'

            else:
                file = open(os.path.expanduser(self.file_path), 'a')
                season, age = IMDB().get_next_episode(title=title_head)
                data = title_head + '/' + str(season) + '/' + str(age)
                file.write(data + '\n')
                file.close()
                print '\n' + title_head.upper() + ' has been added.'
                if age is not None:
                    print '\nThe new episode will air on ' + age
                    print '\n' + 'New torrent will be downloaded automatically.'
                else:
                    print '\nThe new episode air date is not out yet.'
                    print '\nNew torrent will be downloaded when the air date arrives.'

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
                print '\nYou are not following ' + title_head.upper()
                print '\nUse the commnad ADD <title> to start following'

            self.search_query()

        elif re.match(r'info\b', query, flags=re.IGNORECASE):
            print '\nGetting information...'
            i = IMDB()
            title_head = query[5:].strip()
            title, season, age = i.get_latest_episode(title=title_head)

            print '\nCurrent Episode Details'
            if age is None:
                print '\n Information not available yet'
            else:
                print '\n Title : ' + str(title).upper()
                print '\n Episode : ' + str(season).upper()
                print '\n Air Date : ' + age

            season, age = i.get_next_episode(title=title_head)
            print '\nNext Episode details : '
            if age is None:
                print '\n Information not available yet'
            else:
                print '\n Episode : ' + str(season).upper()
                print '\n Air Date : ' + age

            self.search_query()

        elif re.match(r'print\b', query, flags=re.IGNORECASE):
            if os.path.isfile(os.path.expanduser(self.file_path)):
                file = open(os.path.expanduser(self.file_path), 'r')
                lines = file.readlines()
                file.close()
                for line in lines:
                    title = str(line).split('/')[0].strip()
                    print title
            else:
                print '\nYou are not following anything'
                print '\nUse the commnad ADD <title> to start following'

            self.search_query()

        elif re.match(r'top\b', query, flags=re.IGNORECASE):
            print '\nFetching data...'
            title_head = query[4:].strip()
            result = IMDB_TOP().top_items(type=title_head)
            if not result:
                print '\nSorry the following keyword is not present.\nPlease try again'
            self.search_query()
        else:
            try:
                Download_Torrent().search_begins_kat(name=query, boolean=True)
                self.search_query()
            except:
                print '\nSorry torrent can not be downloaded.\nPlease Try again'
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
