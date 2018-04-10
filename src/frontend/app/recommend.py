import pymysql.cursors
import pymysql as mysql
import csv
import string
import vectorSimilarity as vs
import random


def getSimilarSongs(v,simlist):
	sortlist=sorted(simlist, key=lambda x: x[2],reverse=True)
	looklist=[]
	outlist=[]
	for i in range(15):
		x=sorted(vs.parseVectorToDictionary(sortlist[i][1]).iteritems(), key=lambda (k,v): (float(v),k),reverse=True)
		looklist.append((x,sortlist[i][2]))
	index=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	for i in range(15):
		while True:
			mymax=0
			mindex=0
			for j in range(5):
				val=float(looklist[j][1])*(1/(index[j]+j/2.0+1))
				if(val>mymax):
					try:
						a=looklist[j][0][index[j]+1][0]
						mymax=val
						mindex=j
					except:
						print "Error"
			index[mindex]+=1
			key=looklist[mindex][0][index[mindex]][0]

			if not v.has_key(key) and key not in outlist:
				outlist.append(key)
				break
	
	return outlist


def recommendSongs(userid1):
	conn = mysql.connect(
			host='localhost',
			user='root',
			passwd='root',
			db='MRS1',
			charset='utf8'
	)
	cursor = conn.cursor()
	try:
		cursor.execute('SELECT * FROM similarity WHERE userid1="'+userid1+'"')
		similarities=cursor.fetchall()
		simlist=[]
		cursor.execute('SELECT * FROM songvectors')
		songvectors=cursor.fetchall()
		
		cursor.execute('SELECT * FROM songvectors WHERE userid="'+userid1+'"')
		v1=cursor.fetchall()
		v1=v1[0][1]
		for i in range(len(similarities)):
				v2=songvectors[i]
				sim=similarities[i][2]
				simlist.append((v2[0],v2[1],sim))
		simsongs=getSimilarSongs(vs.parseVectorToDictionary(v1),simlist)
		""""for i in range(len(simlist)): 
			print simlist"""
		for i in range(len(simsongs)):
			cursor.execute("SELECT * FROM traindex WHERE ind='"+str(simsongs[i])+"';");
			songid=cursor.fetchall()
			cursor.execute("SELECT artistname,trackname FROM songs WHERE trackid='"+ songid[0][1]+"';");
			songdata=cursor.fetchall()
			simsongs[i]=songdata[0]
		print simsongs
	finally:
		conn.close()
	return simsongs

