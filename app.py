from flask import Flask, render_template, flash, request, redirect, url_for
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

@app.route('/myprofile')
def myprofile():
	return render_template('myprofile.html', username = cu.username, email = cu.email)

@app.route('/rooms')
def rooms():
	return render_template('rooms.html')

@app.route('/creategame')
def creategame():
	return render_template('create_game.html')

@app.route('/game')
def game():
	if not cu.is_login():
		return redirect(url_for('login'))

	with sqlite3.connect("database.db") as con:
		cur = con.cursor()
		cur.execute("select mygame from user WHERE username = ?", (cu.username))
		con.commit()
		game_id = cur.fetchone()[0]
		
		cur.execute("select name, player1, player2, player3, player4 from game WHERE id = ?", (game_id))
		con.commit()
		game = cur.fetchone()[0]
		
		game_name = game[0]
		for i in xrange(1,4):
			p[i-1] = game[i]
		con.close()				
		
		return render_template('game.html', name = game_name, p1 = p[0], p2 = p[1], p3 = p[2], p4 = p[3])


@app.route('/registered', methods = ['POST', 'GET'])
def registered():
   if request.method == 'POST':
   		try:
   			us = request.form['username']
   			em = request.form['email']
   			ps = request.form['password']

   			with sqlite3.connect("database.db") as con:
   				cur = con.cursor()
   				cur.execute("INSERT INTO user (email, username, password) VALUES (?, ?, ?)", (em, us, ps) )
   				con.commit()
   				cur.execute("select id from user WHERE username = ?", (us))
   				con.commit()
   				cu.login()
   				cu.username = us
   				cu.em = em 
   				cu.id = cur.fetchone()[0]
   		except:
   			con.rollback()
   		finally:
   			con.close()
   			return render_template('confirmed_user.html', msg = register_msg)

@app.route('/loggedin', methods = ['POST', 'GET'])
def loggedin():
	if request.method == 'POST':
		try:
			us = request.form['username']
			ps = request.form['password']
			with sqlite3.connect("database.db") as con:
				cur = con.cursor()
				cur.execute("select username, email, id from user WHERE username = ? AND password = ?", (us, ps))
				con.commit()
				user = cur.fetchone()
				if(user == None):
					user_exists = False;
					raise Exception()
				else:
					user_exists = True;
					cu.login()
					cu.username = user[0]
	   				cu.email = user[1]
	   				cu.id = user[2]
		except :
			con.rollback()
		finally:
			con.close()
			return render_template('confirmed_user.html', msg = login_msg)

@app.route('/game_form', methods = ['POST', 'GET'])
def game_form():
	if not cu.is_login():
		return redirect(url_for("login"))

	game_id = -1
	if request.method == 'POST':
		try:
			nm = request.form['name']
			with sqlite3.connect("database.db") as con:
				cur = con.cursor()
				cur.execute("INSERT INTO game (name, player1) VALUES (?, ?)", (nm, cu.id))
				con.commit()
				con.close()
				
			with sqlite3.connect("database.db") as con:
				cur.execute("SELECT g.id FROM game g WHERE g.name = ?", (nm))
				con.commit()
				game_id = cur.fetchone()

				#cur.execute("UPDATE user SET mygame = ? WHERE username = ?", (game_id, cu.username))
				#con.commit()
		except:
			game_id = -2
			con.rollback()
		finally:
			con.close()
			#return redirect(url_for("game"))
			return render_template('confirmed_user.html', msg = game_id)

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 5000)