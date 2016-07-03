import requests
from bs4 import BeautifulSoup

base_url = 'http://www.imdb.com/find?q='
query = 'one+piece'
url = base_url + query

try:
    connection = requests.get(url)
except requests.RequestException as e:
    raise SystemExit('\n' + str(e))

soup = BeautifulSoup(connection.content, 'html5lib')

table = soup.find('table', {'class': 'findList'})
rows = table.findAll('tr')
column = rows[0].findAll('td')
link = column[1].find('a').get('href')
print link
connection.close()

links = link.split('?')
link = links[0] + 'episodes?ref_=tt_ov_epl'
url = 'http://www.imdb.com' + link

try:
    connection = requests.get(url)
except requests.RequestException as e:
    raise SystemExit('\n' + str(e))

soup = BeautifulSoup(connection.content, 'html5lib')
href = soup.find_all('div', {'class': 'info'})
age = soup.find_all('div', {'class': 'airdate'})
link = href[-1].find('a')['href']
title = href[-1].find('a')['title']
print str(age[-1].get_text()).strip()

url = 'http://www.imdb.com' + link
print url
connection.close()
try:
    connection = requests.get(url)
except requests.RequestException as e:
    raise SystemExit('\n' + str(e))

soup = BeautifulSoup(connection.content, 'html5lib')
print title
seasons = soup.find_all('div', {'class': 'bp_heading'})
print seasons[0].get_text()
