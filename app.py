from flask import Flask, render_template, flash, request
import sqlite3
import user

login_msg = "You succsefully logged in!"
register_msg = "You succsefully registered!"

cu = user.Current_user()

app = Flask(__name__)

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/registered', methods = ['POST', 'GET'])
def user():
   if request.method == 'POST':
   		try:
   			us = request.form['username']
   			em = request.form['email']
   			ps = request.form['password']

   			with sqlite3.connect("database.db") as con:
   				cur = con.cursor()
   				cur.execute("INSERT INTO user (email, username, password) VALUES (?, ?, ?)", (em, us, ps) )
   				con.commit()
   				cu.login()
   				cu.username = us
   				cu.em = em 
   		except:
   			con.rollback()
   		finally:
   			con.close()
   			return render_template('user_conformed.html', msg = register_msg)

@app.route('/loggedin', methods = ['POST', 'GET'])
def loggedin():
	if request.method == 'POST':
		try:
			us = request.form['username']
			ps = request.form['password']
			with sqlite3.connect("database.db") as con:
				cur = con.cursor()
				cur.execute("select fname, sname, email, username from user WHERE username = ? AND password = ?", (us, ps))
				con.commit()
				user = cur.fetchone()
				if(user == None):
					user_exists = False;
					raise Exception()
				else:
					user_exists = True;
					cu.login()
					cu.username = user[3]
					cu.fname = user[0]
	   				cu.sname = user[1]
	   				cu.email = user[2]
		except :
			con.rollback()
		finally:
			con.close()
			if(user_exists):
				return render_template('loggedin.html', msg = login_msg)
			else:
				return render_template('wrong_login.html')

if __name__ == '__main__':
   app.run()