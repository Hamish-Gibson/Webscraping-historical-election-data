import requests as rq 
import pandas as pd 
import bs4 as bs 
from scotland_constituencies import constituencies
from tabulate import tabulate 


seat = pd.DataFrame()

#Can only go back this far, page entries change due to constituency boundary changes.
year = ['2010 United Kingdom general election',
        '2015 United Kingdom general election',
        '2017 United Kingdom general election',
        '2019 United Kingdom general election']

#Iterates through each constituency in a given election year.
for election in year: 
    for constituency in constituencies:
        webdata = rq.get(constituencies[constituency])
        webdata = bs.BeautifulSoup(webdata.text, features = 'lxml')
        
        
        #Finds all tables on the page
        tables = webdata.find_all('table', {'class' : 'wikitable'})
        
        for table in tables:
            for element in table.findChildren('caption'):
                #Only considers tables with election data
                if element.findChildren('a', {'title':election}):
                    print('Getting and processing data...')
                    for row in table.find_all('tr', {'class' : 'vcard'}):
                        candidate = [constituency]
                        for column in row.find_all('td')[1:-1]:
                            candidate.append(column.text.strip('\n'))
                        df = {'Constituency': '','Party': '', 'Candidate': '', 
                              'Votes': '', '%':''}
                        for count, key in enumerate(df):
                            df[key] = candidate[count]
                        #Creates row in a dataframe containing the results
                        seat = seat.append(pd.DataFrame(df, index=[election[:4]])) 
        print('Data retrieved for: ', election, 'in',  constituency)
    
pd.set_option('max_colwidth', 20)

print(tabulate(seat,headers='keys',tablefmt='psql'))
