# -*- coding: utf-8 -*-
import pymysql.cursors
import pymysql as mysql
conn = mysql.connect(
    host='localhost',
    user='root',
    passwd='root',
    charset='utf8'
)

cursor = conn.cursor()
cursor.execute('DROP DATABASE IF EXISTS MRS1')	
cursor.execute('CREATE DATABASE IF NOT EXISTS MRS1')
conn.close()

conn = mysql.connect(
    host='localhost',
    user='root',
    passwd='root',
    db='MRS1',
    charset='utf8'
)
try:
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE users (userid VARCHAR(30), gender CHAR(10), age INT, country VARCHAR(300), signup VARCHAR(500), PRIMARY KEY(userid))')
	cursor.execute('CREATE TABLE songs (userid VARCHAR(30), timestamp VARCHAR(300), artistid VARCHAR(500), artistname VARCHAR(300), trackid VARCHAR(500), trackname VARCHAR(300))')
	cursor.execute('CREATE TABLE traindex (ind INT AUTO_INCREMENT, trackid VARCHAR(500), PRIMARY KEY(ind))')
	cursor.execute('CREATE TABLE songvectors (userid VARCHAR(30), songvector MEDIUMBLOB, featurevector MEDIUMBLOB , PRIMARY KEY(userid))')
	cursor.execute('CREATE TABLE similarity (userid1 VARCHAR(30) , userid2 VARCHAR(30) , sim float(50) )')

	import csv
	import string
	with open('../../data/userid-profile-trim.tsv','r') as users:
		users=csv.reader(users,delimiter='\t')
		temp=next(users)
		for user in users:
			for i in range(0,5):
				if user[i]=='':
					user[i]="NULL"
				user[i]=user[i].translate(None, string.punctuation)
			s= 'INSERT INTO users VALUES(\''+str(user[0])+'\',\''+str(user[1])+'\','+str(user[2])+',\''+str(user[3])+'\',\''+str(user[4])+'\')'
			#~ print s
			cursor.execute(s);
	def isEnglish(s):
			try:
					s.decode('ascii')
			except UnicodeDecodeError:
					return False
			else:
					return True
	import csv
	import string
	songlist={}
	with open('../../data/userid-timestamp-artid-artname-traid-traname-trim.tsv','rb') as songs:
		songs=csv.reader(songs,delimiter='\t',quoting=csv.QUOTE_NONE)
		temp=next(songs)
		for song in songs:
			if song[4] == '' :
				#~ print song
				continue
			if song[4] not in songlist:
				songlist[song[4]]=1
				#~ print song
				q= 'INSERT INTO traindex (trackid) VALUES(\''+str(song[4])+'\')'
				#~ print q
				cursor.execute(q);
			for i in [0,3,5]:
				if song[i]=='' or not isEnglish(song[i]):
					song[i]="NULL"
				song[i]=song[i].translate(None, string.punctuation)
			q= 'INSERT INTO songs VALUES(\''+str(song[0])+'\',\''+str(song[1])+'\',\''+str(song[2])+'\',\''+str(song[3])+'\',\''+str(song[4])+'\',\''+str(song[5])+'\')'
			#~ print q
			cursor.execute(q);

	conn.commit()
finally:
	conn.close()
