from flask import Flask, request, render_template, url_for, redirect,session
from werkzeug import secure_filename
import MySQLdb, os
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root: @localhost/blogs'


UPLOAD_FOLDER = os.path.abspath('C:/Users/Moosealok/Desktop/blog_flask/static/uploads/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.secret_key = 'any random string'

@app.route('/')
def index():
	return render_template('sup.html')


@app.route('/visitor/<user>')
def hello_visitor(user):
	return render_template('welcome.html', name=user)

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))







@app.route('/visitorlogin',methods=['POST'])
def visitorlogin():
	username = request.form['username']
	password = request.form['pwd']
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	cursor.execute("SELECT * FROM visitor where username='"+username+"'and password='"+password+"'")
	var = cursor.fetchone()
	session['username']=username
	name=session['username']
	if(var):
		return render_template('welcomev.html',name=name)
	else:
		return "Failure"

@app.route('/bloggerlogin',methods=['POST'])
def bloggerlogin():
	username = request.form['username']
	password = request.form['pwd']
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	cursor.execute("SELECT * FROM blogger where username='"+username+"'and password='"+password+"'")
	var = cursor.fetchone()
	session['username']=username
	name=session['username']
	if(var):
		return render_template('welcomeb.html',name=name)
	else:
		return "Failure"

		
@app.route('/visitorsignup', methods=['POST'])
def visitorsignup():
	name = request.form['name']
	email = request.form['email']
	username = request.form['username']
	pass1 = request.form['pwd1']
	pass2 = request.form['pwd2']
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	try:
		if pass1 == pass2:
			cursor.execute("INSERT INTO visitor (name,email,username,password) VALUES('"+name+"','"+email+"','"+username+"','"+pass1+"')")
			db.commit()
			db.close()
			return redirect(url_for('index'))
		else:
			flash('Passwords do not match')
			return "Failure"
	except Exception as e:
		return "redirect('/404')"

@app.route('/bloggersignup', methods=['POST'])
def bloggersignup():
	name = request.form['name']
	email = request.form['email']
	username = request.form['username']
	pass1 = request.form['pwd1']
	pass2 = request.form['pwd2']
	category = request.form['category']
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	try:
		if pass1 == pass2:
			cursor.execute("INSERT INTO blogger (name,email,username,password,category) VALUES('"+name+"','"+email+"','"+username+"','"+pass1+"','"+category+"')")
			db.commit()
			db.close()
			return redirect(url_for('index'))
		else:
			flash('Passwords do not match')
	except Exception as e:
		return "redirect('/404')"


@app.route('/upload', methods=['POST'])
def upload_file():
	name = request.form['name']
	email = request.form['email']
	category = request.form['category']
	file = request.files['image']
	filename = session['username']
	f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
	file.save(f)
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	path = 'static/uploads/'+file.filename
	cursor.execute("UPDATE blogger set name ='"+name+"', email ='"+email+"', category ='"+category+"', photo ='"+path+"' where username='"+session['username']+"'")
	db.commit()
	db.close()
	return render_template('welcomeb.html')


@app.route('/profile', methods=['GET'])
def profile():
	lname = session['username']
	username = session['username']
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	cursor.execute("SELECT * FROM blogger where username='"+username+"'")
	result = cursor.fetchone()
	if (result):
		name = result[0]
		email = result[3]
		username = result[1]
		category = result[4]
		photo = result[5]
		details={'name':name,'email':email,'username':username,'category':category,'photo':photo}
	db.close()
	return render_template('profile.html',details=details, name=lname)



@app.route('/uploadp',methods=['GET'])
def uploadp():
	name = session['username']
	return render_template('uploadp.html', name=name)

@app.route('/bloggers', methods=['GET'])
def bloggers():
	lname = session['username']
	username = session['username']
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	cursor.execute("SELECT * FROM blogger")
	result = cursor.fetchall()
	results = [] 
	for row in result: 										#for each loop : for (each element) in result:
		dictionary = {'name':row[0],'email':row[3],			#do something to that element
		'category':row[4],'photo':row[5]}
		results.append(dictionary)								
	return render_template("bloggers.html", results=results, name=lname)


@app.route('/bloggersv', methods=['GET'])
def bloggersv():
	lname = session['username']
	username = session['username']
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	cursor.execute("SELECT * FROM blogger")
	result = cursor.fetchall()
	results = [] 
	for row in result: 										#for each loop : for (each element) in result:
		dictionary = {'name':row[0],'email':row[3],			#do something to that element
		'category':row[4],'photo':row[5]}
		results.append(dictionary)								
	return render_template("bloggersv.html", results=results, name=lname)


@app.route('/brands', methods=['GET'])
def brands():
	lname = session['username']
	username = session['username']
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	cursor.execute("SELECT * FROM brand")
	result = cursor.fetchall()
	results = [] 
	for row in result: 										#for each loop : for (each element) in result:
		dictionary = {'name':row[0],'category':row[1],			#do something to that element
		'location':row[2],'photo':row[3]}
		results.append(dictionary)								
	return render_template("brands.html", results=results, name=lname)


@app.route('/brandsv', methods=['GET'])
def brandsv():
	lname = session['username']
	username = session['username']
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	cursor.execute("SELECT * FROM brand")
	result = cursor.fetchall()
	results = [] 
	for row in result: 										#for each loop : for (each element) in result:
		dictionary = {'name':row[0],'category':row[1],			#do something to that element
		'location':row[2],'photo':row[3]}
		results.append(dictionary)								
	return render_template("brandsv.html", results=results, name=lname)


@app.route('/blogs', methods=['GET'])
def blogs():
	lname = session['username']
	username = session['username']
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	cursor.execute("SELECT * FROM blog")
	result = cursor.fetchall()
	results = [] 
	for row in result: 
		cursor1 = db.cursor()
		cursor1.execute("SELECT name FROM blogger where username='"+row[5]+"'")
		name = cursor1.fetchone()										#for each loop : for (each element) in result:
		dictionary = {'heading':row[0],'category':row[1],			#do something to that element
		'content':row[2],'brand':row[3],'photo':row[4],'name':name[0]}
		results.append(dictionary)								
	return render_template("blogs.html", results=results, name=lname)


@app.route('/blogsv', methods=['GET'])
def blogsv():
	lname = session['username']
	username = session['username']
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	cursor.execute("SELECT * FROM blog")
	result = cursor.fetchall()
	results = [] 
	for row in result: 
		cursor1 = db.cursor()
		cursor1.execute("SELECT name FROM blogger where username='"+row[5]+"'")
		name = cursor1.fetchone()										#for each loop : for (each element) in result:
		dictionary = {'heading':row[0],'category':row[1],			#do something to that element
		'content':row[2],'brand':row[3],'photo':row[4],'name':name[0]}
		results.append(dictionary)								
	return render_template("blogsv.html", results=results, name=lname)


@app.route('/postablog', methods=['POST'])
def postablog():
	name = session['username']
	heading = request.form['heading']
	brand = request.form['brand']
	category = request.form['category']
	content = request.form['content']
	file = request.files['image']
	filename = session['username']
	f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
	file.save(f)
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	path = 'static/uploads/'+file.filename
	cursor.execute("INSERT INTO blog (heading,brand,category,content,photo,username) VALUES('"+heading+"','"+brand+"','"+category+"','"+content+"','"+path+"','"+name+"')")
	db.commit()
	db.close()
	return render_template('welcomeb.html', name=name)



@app.route('/bloggerhome', methods=['GET'])
def bloggerhome():
	name=session['username']
	return render_template('welcomeb.html', name=name)

@app.route('/visitorhome', methods=['GET'])
def visitorhome():
	name=session['username']
	return render_template('welcomev.html', name=name)



@app.route('/admin')
def admin():
	return render_template('admin.html')

@app.route('/admin/blogsa')
def blogsa():
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	cursor.execute("SELECT * FROM blog")
	result = cursor.fetchall()
	results = [] 
	for row in result: 
		cursor1 = db.cursor()
		cursor1.execute("SELECT name FROM blogger where username='"+row[5]+"'")
		name = cursor1.fetchone()										#for each loop : for (each element) in result:
		dictionary = {'heading':row[0],'category':row[1],			#do something to that element
		'content':row[2],'brand':row[3],'photo':'/'+row[4],'name':name[0], 'id':row[6]}
		results.append(dictionary)								
	return render_template("blogsa.html", results=results)

@app.route('/deleteblog/<index>',methods=['GET'])
def deleteblog(index):
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	cursor.execute("DELETE FROM blog where id='"+index+"'")
	db.commit()
	db.close()
	return redirect(url_for('blogsa'))

@app.route('/admin/bloggersa', methods=['GET'])
def bloggersa():
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	cursor.execute("SELECT * FROM blogger")
	result = cursor.fetchall()
	results = [] 
	for row in result: 										#for each loop : for (each element) in result:
		dictionary = {'name':row[0],'email':row[3],			#do something to that element
		'category':row[4],'photo':'/'+row[5],'id':row[6]}
		results.append(dictionary)								
	return render_template("bloggersa.html", results=results)

@app.route('/deletebloggera/<index>',methods=['GET'])
def deleteblogger(index):
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	cursor.execute("DELETE FROM blogger where id='"+index+"'")
	db.commit()
	db.close()
	return redirect(url_for('bloggersa'))

@app.route('/admin/brandsa', methods=['GET'])
def brandsa():
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	cursor.execute("SELECT * FROM brand")
	result = cursor.fetchall()
	results = [] 
	for row in result: 										#for each loop : for (each element) in result:
		dictionary = {'name':row[0],'category':row[1],			#do something to that element
		'location':row[2],'photo':'/'+row[3],'id':row[4]}
		results.append(dictionary)								
	return render_template("brandsa.html", results=results)

@app.route('/admin/deletebrand/<index>',methods=['GET'])
def deletebrand(index):
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	cursor.execute("DELETE FROM brand where id='"+index+"'")
	db.commit()
	db.close()
	return redirect(url_for('brandsa'))


@app.route('/addbrand', methods=['POST'])
def addbrand():
	name = request.form['name']
	location = request.form['location']
	category = request.form['category']
	file = request.files['image']
	filename = secure_filename(file.filename)
	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	path = 'static/uploads/'+file.filename
	cursor.execute("INSERT INTO brand (name,category,location,photo) VALUES('"+name+"','"+category+"','"+location+"','"+path+"')")
	db.commit()
	db.close()
	return redirect(url_for('brandsa'))

@app.route('/jobform', methods=['POST'])
def jobform():
	db = MySQLdb.connect("localhost","root","","blogs")
	cursor = db.cursor()
	cursor.execute("SELECT name, id FROM brand")
	result = cursor.fetchall()
	results = [] 
	for row in result: 										#for each loop : for (each element) in result:
		dictionary = {'name':row[0],'id':row[1]}
		results.append(dictionary)								
	return render_template("admin.html", results=results)



if __name__ == "__main__":
   app.run(host="127.0.0.1",port=5000,debug=True)