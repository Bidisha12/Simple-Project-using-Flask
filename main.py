from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegisterForm, EmployeeForm
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, template_folder='templetes')
mysql = MySQL()
key = os.urandom(15)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_EXTENSIONS1 = {'pdf', 'doc','docx','txt'}
app.config['SECRET_KEY'] = key
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'flaskdemo'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['DOCUMENT_FOLDER'] = 'static/document'
mysql.init_app(app)
Bootstrap(app)


@app.route('/') 
def index():
    if 'username' in session:
        sql = "SELECT * FROM employees WHERE delete_flag = 0;"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        empdata = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', data=empdata)
    else:
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    regform = RegisterForm(request.form)
    if request.method == 'POST':
        if regform.validate():
            userdata = request.form
            name = userdata['name']
            email = userdata['email']
            password = userdata['password']
            gender = userdata['gender']
            language = userdata['prolanguage']
            selectsql = "SELECT * FROM users WHERE email = %s;"
            insertsql = "INSERT INTO users(name, email, password, gender, language) VALUES(%s,%s,%s,%s,%s);"
            conn = mysql.connect()
            cursor = conn.cursor()
            rows = cursor.execute(selectsql, (email))
            if rows > 0:
                return 'Email is already registered'
            else:
                rows = cursor.execute(
                    insertsql, (name, email, password, gender, language))
                conn.commit()
                if rows > 0:
                    session['username'] = email
                    return redirect(url_for('index'))
                else:
                    return 'Registration Failed!'
            cursor.close()  # closing the cursor or do not execute the statement letter
            conn.close()  # closing the mysql connection
        else:
            return render_template('register.html', form=regform)
    elif request.method == 'GET':
        return render_template('register.html', form=regform)


@app.route('/login', methods=['GET', 'POST'])
def login():
    fm = LoginForm(request.form)
    if request.method == 'POST':
        if fm.validate():
            logindata = request.form
            username = logindata['username']
            password = logindata['password']
            sql = "SELECT * FROM users WHERE email = %s and password = %s;"
            conn = mysql.connect()
            cursor = conn.cursor()
            rows = cursor.execute(sql,  (username, password))
            conn.commit()
            if rows > 0:
                session['username'] = username
                return redirect(url_for('index'))
            else:
                flash('Invalid username and password')
                return render_template('login.html', form=fm)
            cursor.close()
            conn.close()
        else:
            return render_template('login.html', form=fm)
    elif request.method == 'GET':
        return render_template('login.html', form=fm)


@app.route('/addemp', methods=['GET', 'POST'])
def addemp():
    if 'username' in session:
        form = EmployeeForm(request.form)
        if request.method == 'POST':
            if form.validate():
                empdata = request.form
                firstname = empdata['firstname']
                midname = empdata['midname']
                lastname = empdata['lastname']
                address = empdata['address']
                email = empdata['email']
                mobile = empdata['mobile']
                gender = empdata['gender']
                designation = empdata['designation']
                name = firstname+" "+midname+" "+lastname
                sql = "INSERT INTO employees(name, email, mobile, gender, designation, address) VALUES(%s, %s, %s, %s, %s, %s);"
                conn = mysql.connect()
                cursor = conn.cursor()
                rows = cursor.execute(
                    sql, (name, email, mobile, gender, designation, address))
                conn.commit()
                if rows > 0:
                    flash('Employee Added Successfully')
                    return redirect(url_for('addemp'))
                else:
                    flash('Failed to added new employee!')
                    return redirect(url_for('addemp'))
                cursor.close()
                conn.close()
            else:
                return render_template('addemployee.html', form=form)
        elif request.method == 'GET':
            return render_template('addemployee.html', form=form)
    else:
        return redirect(url_for('login'))


@app.route('/delete/<id>')
def delete(id):
    if 'username' in session:
        sql = "UPDATE employees SET delete_flag = 1 WHERE id = %s;"
        conn = mysql.connect()
        cursor = conn.cursor()
        rows = cursor.execute(sql, (id))
        conn.commit()
        if rows > 0:
            flash('Deleted Successfully')
            return redirect(url_for('index'))
        else:
            flash('Delete Failed')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if 'username' in session:
        form = EmployeeForm(request.form)
        if request.method == 'POST':
            if form.validate():
                empdata = request.form
                firstname = empdata['firstname']
                midname = empdata['midname']
                lastname = empdata['lastname']
                address = empdata['address']
                email = empdata['email']
                mobile = empdata['mobile']
                gender = empdata['gender']
                designation = empdata['designation']
                name = firstname+" "+midname+" "+lastname
                sql = "UPDATE employees SET name = %s, email = %s, mobile = %s, gender = %s, designation = %s, address = %s WHERE id = %s;"
                conn = mysql.connect()
                cursor = conn.cursor()
                rows = cursor.execute(
                    sql, (name, email, mobile, gender, designation, address, id))
                conn.commit()
                if rows > 0:
                    flash('Employee Updated Successfully')
                    return redirect(url_for('index'))
                else:
                    flash('Failed to update employee!')
                    return redirect(url_for('index'))
                cursor.close()
                conn.close()
            else:
                return render_template('edit.html', form=form, id=id)
        elif request.method == 'GET':
            sql = "SELECT * FROM employees WHERE id = %s;"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, (id))
            data = cursor.fetchone()
            fullname = data[1].split(" ")
            ln = len(fullname)
            if ln > 2:
                form.firstname.data = fullname[0]
                form.midname.data = fullname[1]
                form.lastname.data = fullname[2]
            else:
                form.firstname.data = fullname[0]
                form.lastname.data = fullname[1]
            form.address.data = data[6]
            form.email.data = data[2]
            form.mobile.data = data[3]
            form.gender.data = data[4]
            form.designation.data = data[5]
            return render_template('edit.html', form=form, id=id)
    else:
        return redirect(url_for('login'))


def allowed_file(filename,extension):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extension


@app.route('/image-upload/<id>', methods=['GET', 'POST'])
def upload_file(id):
    if 'username' in session:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'img' not in request.files:
                flash('No file part')
                return render_template('imageupload.html', id=id)
            file = request.files['img']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return render_template('imageupload.html', id=id)
            if file and allowed_file(file.filename,ALLOWED_EXTENSIONS):
                fullpath = os.path.join(
                    app.config['UPLOAD_FOLDER'], file.filename)
                conn = mysql.connect()
                cursor = conn.cursor()
                sql = "UPDATE employees SET image = %s WHERE id = %s;"
                rows = cursor.execute(sql, (file.filename, id))
                conn.commit()
                if rows > 0:
                    file.save(fullpath)
                    flash('Image uploaded')
                    return redirect(url_for('index'))
            else:
                flash('extension does not match! Pls upload a image file')
                return render_template('imageupload.html',id=id)
        elif request.method == 'GET':
            return render_template('imageupload.html', id=id)
    else:
        return redirect(url_for('login'))

@app.route('/document-upload/<id>', methods=['GET', 'POST'])
def upload_file1(id):
    if 'username' in session:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'doc' not in request.files:
                flash('No file part')
                return render_template('docupload.html', id=id)
            file = request.files['doc']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return render_template('docupload.html', id=id)
            if file and allowed_file(file.filename,ALLOWED_EXTENSIONS1):
                fullpath = os.path.join(
                    app.config['DOCUMENT_FOLDER'], file.filename)
                conn = mysql.connect()
                cursor = conn.cursor()
                sql = "UPDATE employees SET document = %s WHERE id = %s;"
                rows = cursor.execute(sql, (file.filename, id))
                conn.commit()
                if rows > 0:
                    file.save(fullpath)
                    flash('Document uploaded')
                    return redirect(url_for('index'))
            else:
                flash('extension does not match! Pls upload a document file')
                return render_template('docupload.html',id=id)
        elif request.method == 'GET':
            return render_template('docupload.html', id=id)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
