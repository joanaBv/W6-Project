#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from random import randint
from time import sleep
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
from sklearn import cluster, datasets
from sklearn.preprocessing import StandardScaler
from matplotlib.lines import Line2D
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from random import choice


# In[2]:


secrets_file = open("secrets.txt","r")
string = secrets_file.read()
secrets_dict={}
for line in string.split('\n'):
    if len(line) > 0:
        secrets_dict[line.split(':')[0]]=line.split(':')[1]
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=secrets_dict['cid'],
                                                           client_secret=secrets_dict['csecret']))


# In[9]:


hot_100 = pd.read_csv('hot_100.csv')
master_playlist = pd.read_csv('master_playlist.csv')
final_master_playlist = pd.read_csv('final_master_playlist.csv')


# In[7]:


def get_features_song(song_title):
    
    results = sp.search(q=song_title, limit=1)
    song_uri = results['tracks']['items'][0]["uri"]
    song_af = sp.audio_features(song_uri)
    song_af_df = pd.DataFrame(song_af)
    song_af_df = song_af_df.drop(['type','id','uri','track_href','analysis_url','duration_ms','time_signature'], axis=1)
    song_af_df = StandardScaler().fit_transform(song_af_df)
    
    return (song_af_df)

def get_cluster_song(song_title):
    
    song=get_features_song(song_title)
    cluster = kmeans.predict(song)
    
    return (cluster)


# In[14]:


X = master_playlist.drop(['Artists','Song Title','Unnamed: 0'], axis=1)
X_prep = StandardScaler().fit_transform(X)

kmeans = KMeans(n_clusters=5, random_state=0).fit(X_prep)


# In[15]:


song_title, artist_name = input("Enter song title and artist name separated by a comma: ").lower().split(",")
print("song title: ", song_title)
print("artist name: ", artist_name.strip())
    
from random import choice
answer = 'y'
    
while answer == 'y':
    if (len(hot_100[hot_100['title'].str.contains(song_title)])>0):
        input_index = hot_100.index[hot_100['title'] == song_title].tolist()
        output_index = choice([i for i in range(0,9) if i not in [input_index]])
        print('Try listening to: ' + hot_100['title'].values[output_index] + ' by ' +  hot_100['artist'].values[output_index])
        answer = input("Do you want another suggestion? y/n ").lower()
    else:
        input_cluster = get_cluster_song(song_title)
        temp_df = final_master_playlist[final_master_playlist['cluster'] == input_cluster[0]]
        output_index = randint(0,len(temp_df))
        print('Try listening to: ' + temp_df['song'].values[output_index] + ' by ' +  temp_df['artists'].values[output_index])
        answer = input("Do you want another suggestion? y/n ").lower()
    

