import pip
from ADT import command,automate
try:
    from bs4 import BeautifulSoup
except ImportError:
    pip.main(['install', 'BeautifulSoup4'])

try:
    import tabulate
except ImportError:
    pip.main(['install', 'tabulate'])

try:
    import requests
except ImportError:
    pip.main(['install', 'requests'])

try:
    import evdev
except ImportError:
    pip.main(['install', 'evdev'])

if __name__ == '__main__':
    print 'Initializing script...'
    automate.Automate().begin()
    command.Command().search()
