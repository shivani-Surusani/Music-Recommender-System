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
