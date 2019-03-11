import urllib2
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://basketballmonster.com/playerrankings.aspx'

html = urllib2.urlopen(url).read()
soup = BeautifulSoup(html,'lxml')

soup.findAll('div', class_='results-table')[0].findAll('th', limit=30)

column_headers = [th.getText() for th in soup.findAll('div', class_='results-table')[0].findAll('th', limit=30)]

column_headers = [x.encode('utf-8') for x in column_headers]

data_rows = soup.findAll('div', class_='results-table')[0].findAll('td')

#get the ones where class is not empty

player_data =[]
columns = ['Round', 'Rank', 'Value', 'Name', 'Inj', 'Team', 'Pos', 'g', 'm/g', 'p/g', '3/g', 'r/g', 'a/g', 's/g', 'b/g', 'fg%', 'fga/g', 'ft%', 'fta/g', 'to/g', 'pV', '3V', 'rV', 'aV', 'sV', 'bV', 'fg%V', 'ft%V', 'toV']

player_data = pd.DataFrame(columns=columns)

for i in range(0, len(data_rows)):
    if i == 0:
        
        print(data_rows[i])

print(player_data)


while(attribute < 30):
    player_row = []
    for i in range(0,10):#len(data_rows)):
        print(data_rows[i])
        #if (data_rows[i] != data_rows[0]):
            #player_row = player_row.append(data_rows[i])
    player_data.append(player_row)
    attribute+=1

#for row in data_rows:
#    print(row)
