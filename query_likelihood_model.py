import pandas as pd
import sqlite3
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

# Query Likelihoood Model implementation
def QueryLikelihoodModel(query_tokens):
    print("Query Likelihood model invoked")
    word = stemmer.stem(query_tokens[0])
    output_df = (unigramprob_df.loc[unigramprob_df['word']==word])
    output_df.drop(['word'],axis=1,inplace=True)
    output_df.rename(columns={"count": "prob"},inplace=True)

    for i in range(1,len(query_tokens)):
        word = stemmer.stem(query_tokens[i])
        output_df = pd.merge(output_df,unigramprob_df.loc[unigramprob_df['word']==word],on='track_id')
        output_df['prob'] = output_df['prob']*output_df['count']
        output_df.drop(['word','count'],axis=1,inplace=True)

    return output_df

# Set of stop words
stop_words = set(stopwords.words('english'))

# Initialize a stemmer
stemmer = SnowballStemmer("english")
 
# Read from the dataframe pickle
print("reading the datasets from the pickle file")
song_df = pd.read_pickle('song_list.pickle')
unigramprob_df = pd.read_pickle('unigram_prob.pickle')

while True:
    print("Enter the query")
    query = input()
    query = query.lower()
    
    # Remove stopwords from the input query and tokenize
    query_tokens = query.split(' ')
    query_tokens = [w for w in query_tokens if not w in stop_words]

    # Print the top 10 probabilities
    if len(query_tokens)==0:
        print('invalid query! query contains only stopwords')
    else:
        output_df = QueryLikelihoodModel(query_tokens)
        output_df = pd.merge(output_df,song_df,on='track_id')
        print(output_df.nlargest(10,'prob'))
