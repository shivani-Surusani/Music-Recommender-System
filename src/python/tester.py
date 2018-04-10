import pymysql.cursors
import pymysql as mysql
import songVectors as sv
import csv
import string
import vectorSimilarity as vs
import songVectors as sv
import random

#Parameters
alpha=1
mode = 5 # Mode 1: Top song removed. Mode 2: Top 2 songs removed. Mode 3: 1 of top 3 songs removed at random
# Mode 4: Top 3 songs removed.
flag = 1 # Change in makeSongVectors to see changes
normalizer = 0.03 #Change in makeSongVectors to see changes


def modify(t1,mode):
	x=sorted(t1.iteritems(), key=lambda (k,v): (float(v),k),reverse=True)
	remv=[]
	if(mode == 1):
		for (k,v) in x:
			del t1[k]
			remv.append(k)
			break;
	if(mode == 2):
		b=False
		for (k,v) in x:
			del t1[k]
			remv.append(k)
			if b:
				break;
			b=True
	if(mode == 3):
		remvVal=int(3*random.random())
		count=0
		for (k,v) in x:
			if count==remvVal:
				del t1[k]
				remv.append(k)
				break;
			count+=1
	if(mode == 4):
		count=0
		for (k,v) in x:
			if count>=0 and count <3:
				del t1[k]
				remv.append(k)
			count+=1
	if(mode == 5):
		count=0
		for (k,v) in x:
			if count>=0 and count <4:
				del t1[k]
				remv.append(k)
			count+=1
	return (remv,sv.songVectorToString(t1))


def getSimilarSongs(v,simlist):
	sortlist=sorted(simlist, key=lambda x: x[2],reverse=True)
	looklist=[]
	outlist=[]
	for i in range(10):
		x=sorted(vs.parseVectorToDictionary(sortlist[i][1]).iteritems(), key=lambda (k,v): (float(v),k),reverse=True)
		looklist.append((x,sortlist[i][2]))
	index=[0,0,0,0,0,0,0,0,0,0]
	for i in range(10):
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
	
conn = mysql.connect(
    host='localhost',
    user='root',
    passwd='root',
    db='MRS1',
    charset='utf8'
)
cursor = conn.cursor()
try:
	cursor.execute('SELECT * FROM songvectors')
	songvectors=cursor.fetchall()
	count=0
	miscount=0
	for v1 in songvectors:
		print v1[0]
		if(v1[0]=='user000113'):
			print v1[1]
		simlist=[]
		t1 = vs.parseVectorToDictionary(v1[1])
		(remv,modifiedv1) = modify(t1,mode)
		for v2 in songvectors:
			if(v2[0]!=v1[0]):
				sim=vs.vectorSimilarity(modifiedv1,v2[1],v1[2],v2[2],alpha)
				simlist.append((v2[0],v2[1],sim))
		simsongs=getSimilarSongs(vs.parseVectorToDictionary(modifiedv1),simlist)
		print simsongs
		print remv
		print remv[0] in simsongs or remv[1] in simsongs or remv[2] in simsongs or remv[3] in simsongs  #remv[0] in simsongs or remv[1] in simsongs or remv[2] in simsongs or remv[3] in simsongs
		if remv[0] in simsongs or remv[1] in simsongs or remv[2] in simsongs or remv[3] in simsongs:
			count+=1
		else:
			miscount+=1
	print count*100/149.0
	#~ print miscount
finally:
	conn.close()
