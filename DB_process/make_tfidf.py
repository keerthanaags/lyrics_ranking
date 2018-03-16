import pickle
import pandas as pd
from os import listdir

idf_df = pd.read_pickle('idf.pickle')

for filename in listdir('tf_pickle_files_normalized/'):
    word = filename.split('.')
    tf_df = pd.read_pickle('./tf_pickle_files_normalized/'+filename)
    tf_df[word[0]] = tf_df[word[0]]*(idf_df['IDF'].loc[idf_df['Word']==word[0]].values[0])
    tf_df.to_pickle('vector_space_model/tfidf_pickle_files/'+filename)
