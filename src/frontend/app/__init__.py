#~ from flask import Flask
#~ 
#~ app = Flask(__name__)
#~ app.config.from_object('config')
#~ 
#~ from app import views

from flask import Flask, session, redirect, url_for, escape, request, render_template
from hashlib import md5
import pymysql.cursors
import pymysql as mysql
import helper as hp
import recommend as rc
app = Flask(__name__)

#######################
#   DATABASE CONFIG   #
#######################



@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
	if 'username' in session:
		if request.method == 'POST':
			return redirect(url_for('recommendation'))
		username_session = (session['username'])
		conn = mysql.connect(host='localhost',user='root',passwd='root',charset='utf8',db='MRS1')
		cursor = conn.cursor()
		cursor.execute("SELECT trackid,artistname,trackname FROM songs WHERE userid = %s;", [username_session])
		songs=cursor.fetchall()
		cursor.execute("SELECT * FROM traindex;");
		indices=cursor.fetchall()
		cursor.execute("SELECT songvector FROM songvectors WHERE userid= %s;", [username_session])
		songvector=cursor.fetchall()[0][0]
		cursor.execute("SELECT * FROM users WHERE userid= %s;", [username_session])
		userdata=cursor.fetchall()[0]
		conn.close()
		songdata = hp.songdata(songs,indices,songvector)
		return render_template('index.html', session_user_name=username_session , songdata = songdata, userdata = userdata)
	return redirect(url_for('login'))


@app.route('/recommendation')
def recommendation():
	if 'username' in session:
		username_session = (session['username'])
		conn = mysql.connect(host='localhost',user='root',passwd='root',charset='utf8',db='MRS1')
		
		suggestedsongs=rc.recommendSongs(username_session);
		conn.close()
		return render_template('recommendation.html', session_user_name=username_session , suggestedsongs = suggestedsongs)
	return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if 'username' in session:
		return redirect(url_for('index'))
	if request.method == 'POST':
		username_form  = request.form['username']
		conn = mysql.connect(host='localhost',user='root',passwd='root',charset='utf8',db='MRS1')
		cursor = conn.cursor()
		cursor.execute("SELECT COUNT(1) FROM users WHERE userid = %s;", [username_form]) # CHECKS IF USERNAME EXSIST
		conn.close()
		if cursor.fetchone()[0]:   
			session['username'] = request.form['username']
			return redirect(url_for('index'))
		else:
			error = "Invalid Credential"
	return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
