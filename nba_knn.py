
# coding: utf-8

# In[551]:

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sea
import sqlite3 as sql
import numpy as np
from sklearn import cross_validation
from collections import Counter


con = sql.connect('nba_data.db')
df_advanced = pd.read_sql('SELECT * from advanced_stats', con)
df_teams = pd.read_sql('SELECT * from all_nba_teams', con)
#get the data


# In[552]:

#setup df for join
df_t =  pd.melt(df_teams, id_vars=['year','team'], value_vars=['center','forward 1','forward 2','guard 1','guard 2'])
df_t['player_year'] = df_t['value'].str.rstrip() + df_t['year']
df_t = df_t.set_index(['player_year'])
df_advanced = df_advanced.set_index(['player_year'])


# In[555]:

#join
df = df_advanced.join(df_t[['team','variable']], how='inner').rename(columns = {'team':'All NBA Team'}).drop(['index','PLAYER_ID','TEAM_ID','TEAM_ABBREVIATION','CFID','CFPARAMS','FGM','FGA','FGM_PG','FG_PCT'], axis = 1)


# In[556]:

#clean up df a little more
df = df.rename(columns = {'variable':'Position'})
df = df.reset_index(drop=True)
df['Position'] = df['Position'].map(lambda x: x.rstrip('12').rstrip())


# In[557]:

#unused position specific stuff
#df_center = df[df['Position']=='center']
#df_guard = df[df['Position']=='guard']
#df_forward = df[df['Position']=='forward']


# In[505]:

#just looking at different correlations and position type specific stuff
#sea.pairplot(df[['W_PCT','NET_RATING','DEF_RATING','OFF_RATING','AST_PCT','AST_TO','REB_PCT','TS_PCT','EFG_PCT','USG_PCT','All NBA Team']], hue = 'All NBA Team')
#plt.show()
#for_corr = df.corr()
#print(for_corr)


# In[506]:


#sea.pairplot(df_center[['W_PCT','NET_RATING','DEF_RATING','OFF_RATING','AST_PCT','AST_TO','REB_PCT','TS_PCT','EFG_PCT','USG_PCT','All NBA Team']], hue = 'All NBA Team')
#plt.show()


# In[411]:

#sea.pairplot(df_forward[['W_PCT','NET_RATING','DEF_RATING','OFF_RATING','AST_PCT','AST_TO','REB_PCT','TS_PCT','EFG_PCT','USG_PCT','All NBA Team']], hue = 'All NBA Team')
#plt.show()


# In[507]:

#sea.pairplot(df_guard[['W_PCT','MIN','NET_RATING','DEF_RATING','OFF_RATING','AST_PCT','AST_TO','REB_PCT','TS_PCT','EFG_PCT','USG_PCT','All NBA Team']], hue = 'All NBA Team')
#plt.show()


# In[558]:


#setting knn df W_PCT is the win percentage and PIE is the NBA proprietary player impact estimate found here, http://stats.nba.com/help/glossary/, under PIE
df_knn = df[['PIE','W_PCT','All NBA Team','year']]


# In[559]:

#splitting train and test
train,test = cross_validation.train_test_split(
df_knn, test_size=0.20, random_state=42)


# In[610]:

print(len(train['year']))


# In[560]:

#distance calc
def graphdist(index):
    dist = (((train.ix[index,'PIE']) - x1)**2 + ((train.ix[index,'W_PCT']) - y1)**2)**(1/2)
    dist = round(dist, 6)
    return(dist)



# In[611]:

#df col and list of KNN K values to try 

train['Distance'] = 0
klist = list(range(2,15))
print(klist)
#klist = [1,2]


# In[615]:

correct_count = 0
incorrect_count = 0


acc_kdict = {}


# for every value in my k list
for i in klist:
    #go through each row in my training set
    for index,row in train.iterrows():
        x1 = train.ix[index,'PIE']
        y1 = train.ix[index,'W_PCT']
        correct = row['All NBA Team']
        # for that row take its points and preform a knn for the specified K value
        df = train.drop([index])
        for index,row in df.iterrows():
            df.ix[index, 'distance'] = graphdist(index)
        df = df.sort_values(['distance'], ascending = 1)
        new_df = df.head(n = i)
        team_type = new_df['All NBA Team'].describe()
        #print(row)
        #print(correct)
        #print(team_type['top'])
        #print('----')
        #print(new_df.head(n=i))
        #count how many times the k value found a match versus how many times it didn't for each point in the df
        if team_type['top'] == correct:
            correct_count += 1
        else:
            incorrect_count += 1
    accuracy = correct_count/(incorrect_count+correct_count)
    #append a dict wtih the k vlaue i was testing and how accurate it was 
    acc_kdict.update({i:accuracy})
    #print to show its moving
    print(i)


# In[616]:

#show which preformed the best
print(acc_kdict)


# In[577]:

#need to clean up my graphdist funcation so that the df isn't hard coded
def graphdist_test(index):
    dist = (((test.ix[index,'PIE']) - x1)**2 + ((test.ix[index,'W_PCT']) - y1)**2)**(1/2)
    dist = round(dist, 6)
    return(dist)


# In[619]:

correct_count = 0
incorrect_count = 0
level_two_error = 0

#complete a knn analysis on my test set using the KNN k value shown to work the best on training

for index,row in test.iterrows():
    x1 = test.ix[index,'PIE']
    y1 = test.ix[index,'W_PCT']
    correct = row['All NBA Team']
    df = test.drop([index])
    for index,row in df.iterrows():
        df.ix[index, 'distance'] = graphdist_test(index)
    df = df.sort_values(['distance'], ascending = 1)
    new_df = df.head(n = 13)
    team_type = new_df['All NBA Team'].describe()
    #print(team_type['top'])
    #print(correct)
    #print(team_type['top'])
    #print('----')
    if team_type['top'] == correct:
        correct_count += 1
    else:
        incorrect_count += 1

    


# In[620]:

print(correct_count/(incorrect_count+correct_count))


# In[ ]:

#so about 50% accuracy

