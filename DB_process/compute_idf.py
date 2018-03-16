import pandas as pd
import numpy as np
import pickle
import sqlite3
from os import listdir

df = pd.read_csv('vector_space_model/idfcounts.csv')
print(df)
df['IDF'] = df['IDF'].astype(float)
df['IDF'] = (237645/df['IDF'])
print(df)
df['IDF'] = np.log(df['IDF'])
print(df)
df.to_pickle('idf.pickle')
