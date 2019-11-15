#%%
from bs4 import BeautifulSoup
import requests
import pandas as pd

#%%
url = 'https://basketballmonster.com/playerrankings.aspx'

html = requests.get(url).text
soup = BeautifulSoup(html,'html.parser')



#%%
#cats are in table headers (MEOWW)
#cells are in td

#%%
#get table headers and put into a list
results_table = soup.find('div', {'class': 'results-table'})
results_table_header = results_table.find('thead')
table_headers = results_table_header.find_all('th')

column_headers =[]

for item in table_headers:
    column_headers.append(item.text)

column_headers

#%%
#get individual player's stats
results_table_rows = results_table.find_all('tr')  

player_db = pd.DataFrame(columns = column_headers)

for rows in results_table_rows:
    player_data = []
    player_cells = rows.find_all('td')
    for cell in player_cells:
        player_data.append(cell.text)
    if len(player_data) > 0:
        player_db = player_db.append(pd.Series(player_data, index=column_headers), ignore_index=True) #need to convert to series for column names

#%%
player_db

#%%
#change dtypes
player_db[['Round', 'Rank', 'Value', 'g', 'm/g', 'p/g', '3/g', 'r/g', 'a/g', 's/g', 'b/g', 'fg%', 'fga/g', 'ft%', 'fta/g', 'to/g', 'pV', '3V', 'rV', 'aV', 'sV', 'bV', 'fg%V', 'ft%V', 'toV']] = player_db[['Round', 'Rank', 'Value', 'g', 'm/g', 'p/g', '3/g', 'r/g', 'a/g', 's/g', 'b/g', 'fg%', 'fga/g', 'ft%', 'fta/g', 'to/g', 'pV', '3V', 'rV', 'aV', 'sV', 'bV', 'fg%V', 'ft%V', 'toV']].apply(pd.to_numeric)

#%%
my_team = ['Shai Gilgeous-Alexander', 'C.J. McCollum', 'Otto Porter', 'Montrezl Harrell', 'John Collins', 'Ben Simmons', 'Kristaps Porzingis', "D'Angelo Russell", 'Mitchell Robinson', 'Jason Richardson', 'Myles Turner', 'Cody Zeller', 'P.J. Tucker']

my_players = player_db[player_db['Name'].isin(my_team)]

#%%
my_players.describe()

#%%


#%%
