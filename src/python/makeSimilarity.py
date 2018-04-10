import pymysql.cursors
import pymysql as mysql
import songVectors as sv
import csv
import string
import vectorSimilarity as vs

conn = mysql.connect(
    host='localhost',
    user='root',
    passwd='root',
    db='MRS1',
    charset='utf8'
)
cursor = conn.cursor()
cursor.execute('DROP TABLE similarity')
cursor.execute('CREATE TABLE similarity (userid1 VARCHAR(30) , userid2 VARCHAR(30) , sim float(50))')
try:
	cursor.execute('SELECT * FROM songvectors')
	songvectors=cursor.fetchall()
	q='INSERT INTO similarity (userid1,userid2,sim) VALUES(%s,%s,%s)' 
	for v1 in songvectors:
		print v1[0]
		for v2 in songvectors:
			sim=vs.vectorSimilarity(v1[1],v2[1],v1[2],v2[2],0.95)
			cursor.execute(q,(v1[0],v2[0],sim))
	conn.commit()
finally:
	
	conn.close()
