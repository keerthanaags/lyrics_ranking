import pandas as pd
import sqlite3
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import os
import numpy as np
import math

# Compute cosine similarity between two vectors
def cosine_similarity(query_denom,doc_list):
    numerator = 0
    denom = 0
    for n in doc_list:
        numerator+=n
        denom+=n*n
    return numerator/(math.sqrt(denom) * query_denom)

# vector space model implementation
def vector_space_model(query_set):
    raw_df = pd.DataFrame([])
    query_denom = math.sqrt(len(query_set))
    for word in query_set:
        if os.path.exists('./tfidf_pickle_files/'+word+'.pickle'):
            word_df = pd.read_pickle('./tfidf_pickle_files/'+word+'.pickle')
            if raw_df.empty:
                raw_df = word_df
            else:
                raw_df = raw_df.merge(word_df, on='track_id')
        else:
            raw_df[word]=0.0
    df = raw_df.fillna(0.0)
    df.drop(['track_id'],axis=1,inplace=True)
    df_lists = df.values.tolist()
    del(df)
    i=0
    final_df = pd.DataFrame(columns=['track_id','cosine'])
    for row in df_lists:
        val = cosine_similarity(query_denom,row)
        final_df.loc[i] = [raw_df.iloc[i]['track_id'], val]
        i+=1
    return(final_df.nlargest(10,'cosine'))


#Set of stop words
stop_words = set(stopwords.words('english'))

#Initialize a stemmer
stemmer = SnowballStemmer("english")
 
#Read from the dataframe pickle
print("reading the datasets from the pickle file")
song_df = pd.read_pickle('song_list.pickle')

while True:
    print("Enter the query")
    query = input()
    
    #Remove stopwords from the input query and tokenize
    query_tokens = query.split(' ')
    query_tokens = [w for w in query_tokens if not w in stop_words]

    query_set = set()
    for word in query_tokens:
        query_set.add(stemmer.stem(word))

    if len(query_set)==0:
        print('invalid query! query contains only stopwords')
    else:
        df = vector_space_model(query_set)
        df = pd.merge(df,song_df,on='track_id')
        print(df)
