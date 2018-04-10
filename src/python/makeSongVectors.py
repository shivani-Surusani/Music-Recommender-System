import pymysql.cursors
import pymysql as mysql
import songVectors as sv
import EM 
import csv
import string
import sys
def isEnglish(s):
			try:
					s.decode('ascii')
			except UnicodeDecodeError:
					return False
			else:
					return True
					
conn = mysql.connect(
    host='localhost',
    user='root',
    passwd='root',
    db='MRS1',
    charset='utf8'
)
cursor = conn.cursor()
cursor.execute('DROP TABLE songvectors')
cursor.execute('CREATE TABLE songvectors (userid VARCHAR(30), songvector MEDIUMBLOB, featurevector MEDIUMBLOB , PRIMARY KEY(userid))')

indexdict={}
userdict={}
songvectordict={}
featurevectordict={}
try:
	#~ songswithids=cursor.execute('SELECT * FROM artindex WHERE artistid=\'3febfc09-8ab9-4c4d-896a-7099d2448188\'')
	#~ print cursor.fetchall()
	cursor.execute('SELECT * FROM users')
	users = cursor.fetchall()
	for i in users:
		userdict[i[0]]=i
	cursor.execute('SELECT * FROM traindex')
	indices = cursor.fetchall()
	for i in indices:
		indexdict[i[1]]=i[0]
	with open('../../data/userid-timestamp-artid-artname-traid-traname-trim.tsv','rb') as songs:
		songs=csv.reader(songs,delimiter='\t',quoting=csv.QUOTE_NONE)
		temp=next(songs)
		for song in songs:
			if song[4] == '' :
				continue
			for i in [0,3,5]:
				if song[i]=='' or not isEnglish(song[i]):
					song[i]="NULL"
				song[i]=song[i].translate(None, string.punctuation)
			#Can work with timestamps. But choosing not to right now
			if song[0] not in songvectordict:
				songvectordict[song[0]]={}
				featurevectordict[song[0]]=sv.featureVector(userdict[song[0]])
			if indexdict[song[4]] not in songvectordict[song[0]]:
				songvectordict[song[0]][indexdict[song[4]]]=1 #Just keeping a count for now
			else:
				songvectordict[song[0]][indexdict[song[4]]]+=1
		songvectordict = EM.EM(songvectordict,int(sys.argv[1]),0.003)
		q='INSERT INTO songvectors (userid,songvector,featurevector) VALUES (%s,%s,%s)'
		for user in users:
			s=sv.songVectorToString(songvectordict[user[0]])
			f=sv.featureVectorToString(featurevectordict[user[0]])
			cursor.execute(q,(user[0],s,f))
			#~ print featurevectordict
		conn.commit()
finally:
	
	conn.close()

