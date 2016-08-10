
# coding: utf-8

# In[309]:

import requests
import pandas as pd
import time

HEADERS = {
    'Accept':'application/json, text/plain, */*'
    ,'Accept-Encoding':'gzip, deflate, sdch'
    ,'Accept-Language':'en-US,en;q=0.8'
    ,'Connection':'keep-alive'
    ,'Host':'stats.nba.com'
    ,'Referer':'http://stats.nba.com/league/player/'
    ,'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
}


parameters = {
    'College':''
    ,'Conference':''
    ,'Country':''
    ,'DateFrom':''
    ,'DateTo':''
    ,'Division':''
    ,'DraftPick':''
    ,'DraftYear':''
    ,'GameScope':''
    ,'GameSegment':''
    ,'Height':''
    ,'LastNGames':'0'
    ,'LeagueID':'00'
    ,'Location':''
    ,'MeasureType':'Advanced'
    ,'Month':'0'
    ,'OpponentTeamID':'0'
    ,'Outcome':''
    ,'PORound':'0'
    ,'PaceAdjust':'N'
    ,'PerMode':'Totals'
    ,'Period':'0'
    ,'PlayerExperience':''
    ,'PlayerPosition':''
    ,'PlusMinus':'N'
    ,'Rank':'N'
    ,'Season':'YYYYYY'
    ,'SeasonSegment':''
    ,'SeasonType':'Regular Season'
    ,'ShotClockRange':''
    ,'StarterBench':''
    ,'TeamID':'0'
    ,'VsConference':''
    ,'VsDivision':''
    ,'Weight':''
}

print(type(HEADERS))
print(type(parameters))


parameters['Season'] = '2014-15'
response = requests.get('http://stats.nba.com/stats/leaguedashplayerstats', params=parameters, headers=HEADERS)

#print(response.content)


# In[310]:

start_yr = 1996
end_yr = 2015
yr_list = []

years = range(start_yr,(end_yr+1))
for i in years: 
    scnd_half = str(i+1)[2:]
    yr_list.append(str(i)+"-"+scnd_half)
yr_list[:-1]
print(yr_list)


# In[313]:

big_df = pd.DataFrame()


for i in yr_list:
    
    parameters['Season'] = i
    response = requests.get('http://stats.nba.com/stats/leaguedashplayerstats', params=parameters, headers=HEADERS)


        

    response.raise_for_status()
    stats = response.json()['resultSets'][0]['rowSet']
    headers = response.json()['resultSets'][0]['headers']
    print(len(stats))
    df = pd.DataFrame(stats, columns = headers)
    big_df = big_df.append(df,ignore_index=True)


    
print(big_df.head(n=2))
print(big_df.tail(n=2))




# In[315]:

import sqlite3 as sql


con = sql.connect('nba_data.db')


# In[317]:

df.to_sql('advanced_stats',con, if_exists='replace')


# In[320]:



df2 = pd.read_sql('SELECT * FROM advanced_stats',con)


# In[321]:


print(df2.head())


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



