import requests as rq 
import pandas as pd 
import bs4 as bs 
from scotland_constituencies import constituencies
from tabulate import tabulate 


seat = pd.DataFrame()

year = [
        '2015 United Kingdom general election',
        '2017 United Kingdom general election']
for election in year: 
    for constituency in constituencies:
        webdata = rq.get(constituencies[constituency])
        webdata = bs.BeautifulSoup(webdata.text, features = 'lxml')
        
        #constituency = webdata.find('table', {'class' : 'infobox vcard'})
        #constituency = constituency.find('th').text
        
        tables = webdata.find_all('table', {'class' : 'wikitable'})
        
        for table in tables:
            for element in table.findChildren('caption'):
                if element.findChildren('a', 
                    {'title':election}):
                    print('Getting and processing data...')
                    for row in table.find_all('tr', {'class' : 'vcard'}):
                        candidate = [constituency]
                        for column in row.find_all('td')[1:-1]:
                            candidate.append(column.text.strip('\n'))
                        df = {'Constituency': '','Party': '', 'Candidate': '', 
                              'Votes': '', '%':''}
                        for count, key in enumerate(df):
                            df[key] = candidate[count]
                        seat = seat.append(pd.DataFrame(df, index=[election]))
        print('Data retrieved for: ', election, 'in',  constituency)
    

print(tabulate(seat,headers='keys',tablefmt='psql'))

