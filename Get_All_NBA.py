
# coding: utf-8

# In[19]:

from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3 as sql
import html5lib
import re


# In[20]:

url = 'http://www.basketball-reference.com/awards/all_league.html'
header = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=header)
soup = BeautifulSoup(r.content, "xml")

#print(soup)


# In[36]:

df_list = []

tables = soup.find("table")
for tr in tables.findAll('tr'):
    #print(tr.text)
    #print(type(tr.text))
    temp_list = tr.text.splitlines()
    temp_list = temp_list[1:]
    if len(temp_list)==8:
        df_list.append(temp_list)

cols = ['year','leauge','team','center','forward 1','forward 2','guard 1','guard 2']
df = pd.DataFrame(df_list, columns = cols)

print(df.head())


# In[31]:

df['center'] = df['center'].map(lambda x: x.rstrip('GFCN'))
df['forward 1'] = df['forward 1'].map(lambda x: x.rstrip('GFCN'))
df['forward 2'] = df['forward 2'].map(lambda x: x.rstrip('GFCN'))
df['guard 1'] = df['guard 1'].map(lambda x: x.rstrip('GFCN'))
df['guard 2'] = df['guard 2'].map(lambda x: x.rstrip('GFCN'))


# In[33]:



con = sql.connect('nba_data.db')
df.to_sql('all_nba_teams',con, if_exists='replace')




# In[ ]:



