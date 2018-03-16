import pandas as pd
import sqlite3
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pickle

#Establish DB connection
conn = sqlite3.connect("nlp_project.db")

print('established DB connection.. counting total no. of words in each track')
#Total no. of words in each track
total_count_df = pd.read_sql_query("select track_id,sum(count) counts from lyrics_no_stopwords group by track_id;", conn)

print('reading the dataset')
#Lyrics dataset
lyrics = pd.read_sql_query("select * from lyrics_no_stopwords;",conn)

print('merging the dataframes and computing unigram probabilities')
#Merge the two dataframes and compute probability for each word in a track
merged = pd.merge(lyrics,total_count_df,on='track_id')
merged['count'] = merged['count']/merged['counts']

#Drop the useless columns
merged.drop(['counts','mxm_tid','is_test'],axis=1,inplace=True)

print('reading the song lists')
#get songnames
song_df = pd.read_sql_query("select * from songs;",conn)
song_df.drop(['mxm_id'],axis=1,inplace=True)

print('pickling the dataframes song_list and unigram_prob')
song_df.to_pickle('song_list.pickle')
merged.to_pickle('unigram_prob.pickle')
