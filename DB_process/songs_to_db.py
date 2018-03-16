#!/usr/bin/env python
import os
import sys
import sqlite3

# params
trainf = sys.argv[1]
outputf = sys.argv[2]

# sanity checks
if not os.path.isfile(trainf):
    print 'ERROR: %s does not exist.' % trainf
    sys.exit(0)

# connect to db
conn = sqlite3.connect(outputf)

# create table
q = "CREATE TABLE songs (track_id varchar(20), mxm_id varchar(10), track_name varchar(25), artist_name varchar(25))"
conn.execute(q)

# insert into table
filename = trainf
content = open(filename,'r').readlines()
for line in content:
    line_tokens = line.split("<SEP>")
    line_tokens[1] = line_tokens[1].replace("\"","\"\"")
    line_tokens[2] = line_tokens[2].replace("\"","\"\"")
    q = "INSERT INTO songs VALUES(\""
    q += line_tokens[0] + "\",\""
    q += line_tokens[3] + "\",\""
    q += line_tokens[2] + "\",\""
    q += line_tokens[1] + "\")"
    print(q)
    conn.execute(q)

conn.commit()
conn.close()
