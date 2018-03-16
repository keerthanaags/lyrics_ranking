import sqlite3
import nltk
from nltk.corpus import stopwords

# Initialize the stopwords
stop = set(stopwords.words('english'))
print(stop)

conn = sqlite3.connect('nlp_project.db')

# Remove stop words from the database
for stop_word in stop:
    query = "DELETE FROM lyrics_no_stopwords WHERE word=\""+stop_word+"\""
    print(query)
    conn.execute(query)
    query = "DELETE FROM words_no_stopwords WHERE word=\""+stop_word+"\""
    print(query)
    conn.execute(query)

conn.commit()
conn.close()

