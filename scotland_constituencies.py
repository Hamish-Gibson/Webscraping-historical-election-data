import requests as rq 
import bs4 as bs 

wiki_page = rq.get('https://en.wikipedia.org/wiki/United_Kingdom_Parliament_constituencies') 
wiki_page = bs.BeautifulSoup(wiki_page.text, features = 'lxml')

tag = wiki_page.find('span', {'class' : 'mw-headline', 
                                  'id' : 'Scotland'})

table = tag.find_parent('h3').next_sibling.next_sibling.next_sibling.next_sibling

constituencies = {}

for row in table.find_all('tr')[1:]:
    key = row.find_all('td')[0].find('a').text
    value = row.find_all('td')[0].find('a')['href']
    constituencies.update({key : value})
    
for key in constituencies:
    constituencies[key] = 'https://en.wikipedia.org/' + constituencies[key]

