import sqlite3

conn = sqlite3.connect('example.db')
c = conn.cursor()
c.execute('Create Table usa_artists_state_location ( artist_id varchar(100) primary key, lat varchar(100), lon varchar(100), state varchar(100));')
a = open('usa_artist_state_location.csv', 'r')
b = a.readlines()
b[0]
b.pop(0)
table = []
for row in b:
    item = row[:-1].split(',')
    table.append((item[0], item[1], item[2], item[3]))

c.executemany('INSERT INTO usa_artists_state_location VALUES(?, ?, ?,  ?) ', table)
conn.commit()

for row in c.execute('SELECT * FROM usa_artists_state_location'):
    print row

conn.close()