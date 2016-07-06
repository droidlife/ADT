import threading, os, sys
from datetime import datetime

def it():
    threading.Timer(5.0, it).start()
    print 'hello'


class Automate:
    def __init__(self):
        self.file_path = None

    def begin(self):
        self._get_file_path()
        if os.path.isfile(os.path.expanduser(self.file_path)):
            file = open(os.path.expanduser(self.file_path), 'r')
            lines = file.readlines()
            file.close()

            for line in lines:
                age = str(line).split('/')
                if '\n' not in age:
                    air_date = age[2].strip()
                    if air_date is not None:
                        date_object = datetime.strptime(air_date, '%d %B %Y')
                        date = datetime.now()
                        days =  str(date_object-date).split(' ')[0]
                        if int(days) < 0:
                            print 'torrent ready for downloading'

    def _get_file_path(self):
        if os.name == 'nt':
            pass
        elif os.uname()[0] == 'Linux':
            self.file_path = '~/.follow'
        elif sys.platform.startswith('darwin'):
            self.file_path = '~/.follow'
