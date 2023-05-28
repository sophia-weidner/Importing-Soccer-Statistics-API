#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import xlrd
from bs4 import BeautifulSoup
import numpy as np


# # Transformation 1
# I am going to use player names from the previous milestone and create a new df from the API using those same players.
# The players I need are:
# Neymar, Mbappe, Coutinho, Felix, Griezmann, Grealish, Lukaku, Dembele, Pogba, and Hazard.

# In[2]:


# Neymar
neymar = requests.get('https://www.thesportsdb.com/api/v1/json/2/searchplayers.php?p=Neymar') # %20 for space.
x = neymar.json()
neymar_df = pd.DataFrame(x['player'])

# Mbappe
mbappe = requests.get('https://www.thesportsdb.com/api/v1/json/2/searchplayers.php?p=Kylian%20Mbappe')
x2 = mbappe.json()
mbappe_df = pd.DataFrame(x2['player'])

# Coutinho
coutinho = requests.get('https://www.thesportsdb.com/api/v1/json/2/searchplayers.php?p=Philippe%20Coutinho')
x3 = coutinho.json()
coutinho_df = pd.DataFrame(x3['player'])

# Felix
felix = requests.get('https://www.thesportsdb.com/api/v1/json/2/searchplayers.php?p=Joao%20Felix')
x4 = felix.json()
felix_df = pd.DataFrame(x4['player'])

# Griezmann
griezmann = requests.get('https://www.thesportsdb.com/api/v1/json/2/searchplayers.php?p=Antoine%20Griezmann')
x5 = griezmann.json()
griezmann_df = pd.DataFrame(x5['player'])

# Grealish
grealish = requests.get('https://www.thesportsdb.com/api/v1/json/2/searchplayers.php?p=Jack%20Grealish')
x6 = grealish.json()
grealish_df = pd.DataFrame(x6['player'])

# Lukaku
lukaku = requests.get('https://www.thesportsdb.com/api/v1/json/2/searchplayers.php?p=Romelu%20Lukaku')
x7 = lukaku.json()
lukaku_df = pd.DataFrame(x7['player'])

# Dembele
dembele = requests.get('https://www.thesportsdb.com/api/v1/json/2/searchplayers.php?p=Ousmane%20Dembele')
x8 = dembele.json()
dembele_df = pd.DataFrame(x8['player'])

# Pogba
pogba = requests.get('https://www.thesportsdb.com/api/v1/json/2/searchplayers.php?p=Paul%20Pogba')
x9 = pogba.json()
pogba_df = pd.DataFrame(x9['player'])

# Hazard
hazard = requests.get('https://www.thesportsdb.com/api/v1/json/2/searchplayers.php?p=Eden%20Hazard')
x10 = hazard.json()
hazard_df = pd.DataFrame(x10['player'])


# In[3]:


# Neymar, Mbappe, Coutinho, Felix, Griezmann, Grealish, Lukaku, Dembele, Pogba, and Hazard.
frames = [neymar_df, mbappe_df, coutinho_df, felix_df, griezmann_df, grealish_df, lukaku_df, dembele_df,
         pogba_df, hazard_df]

df = pd.concat(frames)


# In[4]:


df.head()


# # Transformation 2
# I am going to remove Fanart columns; they are unnecessary regarding the original goal of my project.\

# In[5]:


list(df.columns)
df_1 = df.drop(['strFanart1', 'strFanart2', 'strFanart3', 'strFanart4'], axis=1)
df_1.head()


# # Transformation 3
# I am going to remove more columns.

# In[6]:


list(df_1.columns)


# In[7]:


df_2 = df_1.drop(['strDescriptionDE', 'strDescriptionFR', 'strDescriptionCN', 'strDescriptionIT',
                  'strDescriptionJP','strDescriptionRU','strDescriptionES','strDescriptionPT','strDescriptionSE',
                  'strDescriptionNL','strDescriptionHU','strDescriptionNO','strDescriptionIL','strDescriptionPL',], 
                 axis=1)

# I am dropping player descriptions in various languages, except I am keeping English - simply because I do not
# understand other languages and it is the same sentence(s) translated over and over again.


# In[8]:


df_2.head()


# In[9]:


df_3 = df_2.drop(['idPlayer','idTeam','idTeam2','idTeamNational'], axis=1)


# In[10]:


df_3.head()


# # Transformation 3
# I am going to drop the 'id', 'str' and 'int' in front of the column names.

# In[11]:


df_3.columns = df_3.columns.str.replace('str', '')


# In[12]:


df_3.columns = df_3.columns.str.replace('id', '')


# In[13]:


df_3.columns = df_3.columns.str.replace('int', '')


# In[14]:


list(df_3.columns)


# # Transformation 4
# I am going to reorder some columns based on what I believe to be important information. For example, I am going to make sure their name is the first column, followed by nationality, team, position, etc.

# In[15]:


df_4 = df_3[['Player', 'Nationality', 'Team', 'Team2', 'Position', 'Wage', 'dateSigned', 
             'SoccerXML','APIfootball','PlayerManager','PlayerAlternate','Sport','SoccerXMLTeamID','dateBorn',
             'Number','Signing','Outfitter','Kit','Agent','BirthLocation','Ethnicity','Status','DescriptionEN',
             'Gender','Se','College','Facebook','Website','Twitter','Instagram','Youtube','Height','Weight',
             'Loved','Thumb','Cutout','Render','Banner','CreativeCommons','Locked']]


# In[16]:


df_4.head()


# # Transformation 5
# I am going to search for any NaN values or any blank values and replace them with 'none'. I am going to leave 'none' lowercase to indiciate that I went through and changed the value; it wasn't the value that was imported from the API.

# In[17]:


df_4.isnull().values.any()


# In[18]:


df_4.isnull()


# In[19]:


df_5 = df_4.fillna('none')


# In[20]:


df_5.isnull()


# In[21]:


# When investigating NA values, I see that the wage column has some blank spaces. I am just going to take a deeper
# look at this to see if there's something going on. I may end up dropping the column altogether.

print(df_5['Wage'])

# Since there's only 2 values and the rest are blank spaces, I am going to remove this column.

df_6 = df_5.drop(['Wage'], axis = 1)


# In[22]:


df_6.head()


# In[23]:


# There are other rows with blank spaces. I may have to replace them or drop them, but I will leave them for now
# and make those decisions during the final milestone while visualizing the data.


# # Ethical Implications
# 
# ### Milestone 3:
# During milestone 3, I created new columns to show the USD amount of money as opposed to Euros. I made sure to keep the Euros column, however, this still leaves room for mistakes. For example, I had to Google how to convert Euros to USD, and I simply just took the columns and multiplied them by 1.13 to get that answer. I also didn't round the answers. Ethically, I shouldn't use this data to create any visualizations or draw any conclusions from it as it may not be entirely accurate. I just wanted to have the USD columns for reference, but any analysis of the data should fully utilize the Euros columns.
# 
# ### Milestone 4:
# The API I used has a wide range of sports, players, tournaments, etc. I only used a small bit of it compared to the larger pool of information there is. And, even in this small bit, there is a lot of missing data. I dropped what I thought I didn't need, as those columns did not have much in common with the other dataframes I have created thus far. There are some columns here that do have certain information about some players that I do need; however, in those columns, there aren't values for certain players. I feel like this is ethically challenging because I can't compare these players on an even playing field. For example, I would've really liked to have kept the Wage column, but only Neymar and Grealish had that information available. I can't accurately compare the wages between the players, so I just dropped the column altogether. There are other columns that are in a similar fashion, but only have blank spaces for 1 or 2 players. I will need to make a decision when visualizing the data on whether I can ethically use that information to draw any conclusions.

# In[24]:


df_6.columns.tolist()


# In[25]:


df_6.to_csv(r'/Users/sophiaweidner/Downloads/df_5.csv', index=False)


# In[ ]:




