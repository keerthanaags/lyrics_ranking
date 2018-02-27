import pandas as pd
import sqlite3
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#Set of stop words
stop_words = set(stopwords.words('english'))
 
#Establish DB connection
conn = sqlite3.connect("nlp_project.db")

#Total no. of words in each track
total_count_df = pd.read_sql_query("select track_id,sum(count) counts from lyrics_no_stopwords group by track_id;", conn)

#get songnames
song_df = pd.read_sql_query("select * from songs;",conn)
song_df.drop(['mxm_id'],axis=1,inplace=True)

#Lyrics dataset
lyrics = pd.read_sql_query("select * from lyrics_no_stopwords;",conn)

print("Working on preprocessing the dataframe...")

#Merge the two dataframes and compute probability for each word in a track
merged = pd.merge(lyrics,total_count_df,on='track_id')
merged['count'] = merged['count']/merged['counts']

#Drop the useless columns
merged.drop(['counts','mxm_tid','is_test'],axis=1,inplace=True)

#Delete the unnecessary dataframes
del total_count_df
del lyrics

while True:
    print("Enter the query")
    query = input()
    #Remove stopwords from the input query and tokenize
    query_tokens = query.split(' ')
    query_tokens = [w for w in query_tokens if not w in stop_words]

    #Create a final dataframe with tracks containing all the words in the search query
    final_df = (merged.loc[merged['word']==query_tokens[0]])
    final_df.drop(['word'],axis=1,inplace=True)
    final_df.rename(columns={"count": "prob"},inplace=True)

    for i in range(1,len(query_tokens)):
        print("considering",query_tokens[i])
        final_df = pd.merge(final_df,merged.loc[merged['word']==query_tokens[i]],on='track_id')
        final_df['prob'] = final_df['prob']*final_df['count']
        final_df.drop(['word','count'],axis=1,inplace=True)

    #Print the top 10 probabilities
    ranked_df = final_df.nlargest(10,'prob')
    ranked_df = pd.merge(ranked_df,song_df,on='track_id')
    print(ranked_df)
