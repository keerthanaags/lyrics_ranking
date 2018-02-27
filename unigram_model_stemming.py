import pandas as pd
import sqlite3
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

def queryLikelihoodModel(query_tokens):
    print("considering",query_tokens[0])
    primary_df = (unigramprob_df.loc[unigramprob_df['word']==query_tokens[0]])
    primary_df.drop(['word'],axis=1,inplace=True)
    primary_df.rename(columns={"count": "prob"},inplace=True)

    for i in range(1,len(query_tokens)):
        print("considering",query_tokens[i])
        primary_df = pd.merge(primary_df,unigramprob_df.loc[unigramprob_df['word']==query_tokens[i]],on='track_id')
        primary_df['prob'] = primary_df['prob']*primary_df['count']
        primary_df.drop(['word','count'],axis=1,inplace=True)

    return primary_df

def stemmedModel(query_tokens):
    print("Stemmed model invoked")
    print("Considering",query_tokens[0])
    word = stemmer.stem(query_tokens[0])
    print("stemmed word is",word)
    secondary_df = (unigramprob_df.loc[unigramprob_df['word']==word])
    secondary_df.drop(['word'],axis=1,inplace=True)
    secondary_df.rename(columns={"count": "prob"},inplace=True)

    for i in range(1,len(query_tokens)):
        print("considering",query_tokens[i])
        word = stemmer.stem(query_tokens[i])
        print("stemmed word is",word)
        secondary_df = pd.merge(secondary_df,unigramprob_df.loc[unigramprob_df['word']==word],on='track_id')
        secondary_df['prob'] = secondary_df['prob']*secondary_df['count']
        secondary_df.drop(['word','count'],axis=1,inplace=True)

    return secondary_df

#def bestMatchSingleWord(query_tokens):

#Set of stop words
stop_words = set(stopwords.words('english'))

#Initialize a stemmer
stemmer = SnowballStemmer("english")
 
#Read from the dataframe pickle
print("reading the datasets from the pickle file")
song_df = pd.read_pickle('song_list.pickle')
unigramprob_df = pd.read_pickle('unigram_prob.pickle')

while True:
    print("Enter the query")
    query = input()
    
    #Remove stopwords from the input query and tokenize
    query_tokens = query.split(' ')
    query_tokens = [w for w in query_tokens if not w in stop_words]

    #What if the query contains only stop words

    primary_df = queryLikelihoodModel(query_tokens)

    #Print the top 10 probabilities
    prim_len = len(primary_df)
    print(prim_len)

    if prim_len >= 10:
        ranked_df = primary_df.nlargest(10,'prob')
        ranked_df = pd.merge(ranked_df,song_df,on='track_id')
        print(ranked_df)
    else:
        stemmed_df = stemmedModel(query_tokens)
        ranked_df = pd.merge(primary_df,song_df,on='track_id')
        stemmed_df = pd.merge(stemmed_df,song_df,on='track_id')
        print(ranked_df.sort_values(by='prob',ascending=False))
        print(stemmed_df.nlargest(10-prim_len,'prob'))

