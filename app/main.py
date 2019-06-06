import pymysql
from app import app
from tables import Results
from db_configuration import mysql, bcrypt
from flask import flash, render_template, request, redirect, session
from functools import wraps


def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)

		else:
			flash('Please login first!')
			return redirect('/login')
	return wrap


@app.route('/about')
def about_page():
	return render_template('about.html')


@app.route('/')
def index():
		return render_template('index.html')


@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/new_user')
def add_new_user():
	return render_template('add.html')


@app.route('/logout')
@login_required
def logout():
	session.clear()
	flash('You have been logged out.')
	return redirect('/login')


@app.route('/add', methods=['POST'])
def add_user():
	try:		
		usr_name = request.form['inputName']
		usr_email = request.form['inputEmail']
		usr_pass = request.form['inputPassword']
		pw_hash = bcrypt.generate_password_hash(usr_pass).decode('utf-8')
		if usr_name and usr_email and usr_pass and request.method == 'POST':
			sql_query = "INSERT INTO users(user_name, user_email, user_password) VALUES(%s, %s, %s)"
			usr_inp = (usr_name, usr_email, pw_hash)
			cn = mysql.connect()
			cursor = cn.cursor()
			cursor.execute(sql_query, usr_inp)
			cn.commit()
			flash('User added successfully!')
			return redirect('/overview')
		else:
			return 'Error while adding user'
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		cn.close()


@app.route('/submit', methods=['POST'])
def login_submit():
	usr_inp_em = request.form['inputEmail']
	usr_inp_pw = request.form['inputPassword']
	if usr_inp_em and usr_inp_pw and request.method == 'POST':
		cn = mysql.connect()
		cursor = cn.cursor()
		sql_query = "SELECT * FROM users WHERE user_email = %s"
		cursor.execute(sql_query, usr_inp_em)
		row = cursor.fetchone()
		if row:
			if bcrypt.check_password_hash(row[3].encode('utf-8'), usr_inp_pw.encode('utf-8')):
				session['email'] = row[2]
				session['logged_in'] = True
				cursor.close()
				cn.close()
				return redirect('/overview')
			else:
				flash('Invalid password!')
				return redirect('/login')
		else:
			flash('Invalid email/password!')
			return redirect('/login')


@app.route('/overview')
@login_required
def overview():
	try:
		cn = mysql.connect()
		cursor = cn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM users")
		rows = cursor.fetchall()
		table = Results(rows)
		table.border = True
		return render_template('users.html', table=table)
	except Exception as f:
		print(f)
	finally:
		cursor.close() 
		cn.close()


@app.route('/edit/<int:id>')
def edit_view(id):
	try:
		cn = mysql.connect()
		cursor = cn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM users WHERE user_id=%s", id)
		row = cursor.fetchone()
		if row:
			return render_template('edit.html', row=row)
		else:
			return 'Error loading #{id}'.format(id=id)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		cn.close()


@app.route('/update', methods=['POST'])
def update_user():
	try:		
		usr_inp_name = request.form['inputName']
		usr_inp_email = request.form['inputEmail']
		usr_inp_pass = request.form['inputPassword']
		usr_id = request.form['id']
		pw_hash = bcrypt.generate_password_hash(usr_inp_pass).decode('utf-8')
		if usr_inp_name and usr_inp_email and usr_inp_pass and usr_id and request.method == 'POST':
			sql_query = "UPDATE users SET user_name=%s, user_email=%s, user_password=%s WHERE user_id=%s"
			usr_inp = (usr_inp_name, usr_inp_email, pw_hash, usr_id,)
			cn = mysql.connect()
			cursor = cn.cursor()
			cursor.execute(sql_query, usr_inp)
			cn.commit()
			flash('User updated successfully!')
			return redirect('/overview')
		else:
			return 'Error while updating user'
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		cn.close()


@app.route('/delete/<int:id>')
def delete_user(id):
	try:
		cn = mysql.connect()
		cursor = cn.cursor()
		cursor.execute("DELETE FROM users WHERE user_id=%s", (id,))
		cn.commit()
		flash('User deleted successfully!')
		return redirect('/overview')
	except Exception as f:
		print(f)
	finally:
		cursor.close() 
		cn.close()


if __name__ == "__main__":
	app.run()
