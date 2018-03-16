import pandas as pd
import sqlite3
from nltk.corpus import stopwords
import pickle
import sys

word_list = pickle.load(open(sys.argv[1],"rb"))

#Establish DB connection
conn = sqlite3.connect("nlp_project.db")

print('established DB connection.. counting total no. of words in each track')
#Total no. of words in each track
total_count_df = pd.read_sql_query("select track_id,sum(count) counts from lyrics_no_stopwords group by track_id;", conn)

#reading from db to dataframe
print("reading from db to dataframe")
lyrics_df = pd.read_sql_query("select * from lyrics_no_stopwords;", conn)
lyrics_df.drop(['mxm_tid','is_test'],axis=1,inplace=True)
print(lyrics_df)
i=0

print('merging the dataframes and computing unigram probabilities')
#Merge the two dataframes and compute probability for each word in a track
merged = pd.merge(lyrics_df,total_count_df,on='track_id')
merged['count'] = merged['count']/merged['counts']
merged.drop(['counts'],axis=1,inplace=True)


for word in word_list:
    print("considering word no.",i)
    i+=1
    word_df = merged[merged['word']==word]
    word_df.drop(['word'],axis=1,inplace=True)
    word_df.rename(columns={"count": word},inplace=True)
    counts = len(word_df.index)
    with open("idfcounts.csv", "a") as myfile:
            myfile.write(word+","+str(counts)+"\n")
    filename = './tf_pickle_files_normalized/' + word + '.pickle'
    word_df.to_pickle(filename)
