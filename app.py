#!/usr/bin/python3

from flask import Flask, flash, render_template, request, redirect, url_for, session, Response
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import cv2
import numpy as np
import face_recognition
from datetime import datetime
import re
import os
import sys


UPLOAD_FOLDER = 'faces'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
bcrypt = Bcrypt(app)
mysql = MySQL(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        if email and password:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
            user = cursor.fetchone()
            if user and bcrypt.check_password_hash(user['password'], password):
                session['loggedin'] = True
                session['userid'] = user['id']
                session['name'] = user['first_name']
                session['email'] = user['email']
                session['role'] = user['role']
                flash('Logged in successfully!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Email or password is incorrect!', 'error')
        else:
            flash('Missing email or password', 'error')
    return render_template('login.html')

@app.route("/", methods =['GET', 'POST'], strict_slashes=False)
def dashboard():
    if 'loggedin' in session:
        return render_template("dashboard.html")
    return redirect(url_for('login'))

@app.route("/users", methods =['GET', 'POST'])
def users():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user WHERE role = 'user'")
        users = cursor.fetchall()
        return render_template("users.html", users = users)
    return redirect(url_for('login'))

@app.route("/save_user", methods =['GET', 'POST'])
def save_user():
    msg = ''
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST' and 'role' in request.form and 'first_name' in request.form and 'last_name' in request.form and 'email' in request.form :

            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            role = request.form['role']
            action = request.form['action']

            filename = ''
            if 'file' in request.files:
                file = request.files['file']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            if action == 'updateUser':
                userId = request.form['userid']
                cursor.execute('UPDATE user SET first_name= %s, last_name= %s, email= %s, picture= %s, role= %s WHERE id = %s', (first_name, last_name, email, filename, role, (userId, ), ))
                mysql.connection.commit()
            else:
                password = request.form['password']
                cursor.execute('INSERT INTO user (`first_name`, `last_name`, `email`, `password`, `picture`, `role`) VALUES (%s, %s, %s, %s, %s, %s)', (first_name, last_name, email, password, filename, role))
                mysql.connection.commit()

            return redirect(url_for('users'))
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return redirect(url_for('users'))
    return redirect(url_for('login'))

@app.route("/edit_user", methods =['GET', 'POST'])
def edit_user():
    msg = ''
    if 'loggedin' in session:
        editUserId = request.args.get('userid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE id = % s', (editUserId, ))
        users = cursor.fetchall()

        return render_template("edit_user.html", users = users)
    return redirect(url_for('login'))


@app.route("/view_user", methods =['GET', 'POST'])
def view_user():
    if 'loggedin' in session:
        viewUserId = request.args.get('userid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE id = % s', (viewUserId, ))
        user = cursor.fetchone()
        return render_template("view_user.html", user = user)
    return redirect(url_for('login'))

@app.route("/password_change", methods =['GET', 'POST'])
def password_change():
    mesage = ''
    if 'loggedin' in session:
        changePassUserId = request.args.get('userid')
        if request.method == 'POST' and 'password' in request.form and 'confirm_pass' in request.form and 'userid' in request.form  :
            password = request.form['password']
            confirm_pass = request.form['confirm_pass']
            userId = request.form['userid']
            if not password or not confirm_pass:
                mesage = 'Please fill out the form !'
            elif password != confirm_pass:
                mesage = 'Confirm password is not equal!'
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE user SET  password =% s WHERE id =% s', (password, (userId, ), ))
                mysql.connection.commit()
                mesage = 'Password updated !'
        elif request.method == 'POST':
            mesage = 'Please fill out the form !'
        return render_template("password_change.html", mesage = mesage, changePassUserId = changePassUserId)
    return redirect(url_for('login'))

@app.route("/delete_user", methods =['GET'])
def delete_user():
    if 'loggedin' in session:
        deleteUserId = request.args.get('userid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM user WHERE id = % s', (deleteUserId, ))
        mysql.connection.commit()
        return redirect(url_for('users'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userName = request.form.get('name')
        password = request.form.get('password')
        email = request.form.get('email')

        # Validate email format
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', 'error') # Add a category 'error' for styling
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
            account = cursor.fetchone()
            # Check if account already exists
            if account:
                flash('Account already exists!', 'info') # 'info' as a category for informational messages
            else:
                # Attempt to register the user
                try:
                    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                    cursor.execute('INSERT INTO user (name, email, password) VALUES (%s, %s, %s)', (userName, email, hashed_password,))
                    mysql.connection.commit()
                    flash('You have successfully registered!', 'success') # 'success' for successful operations
                except Exception as e:
                    flash('Registration failed due to an internal error. Please try again.', 'error') # Log this exception

        return redirect(url_for('register')) # Redirect back to the registration page to show flash messages

    # For GET requests, or if any other method is used, just show the registration page.
    return render_template('register.html')

@app.route("/attendance", methods =['GET', 'POST'])
def attendance():
    if 'loggedin' in session:
        userId = request.args.get('userid')
        return render_template("attendance.html", userid = userId)
    return redirect(url_for('login'))

def generate(userImage):
    IMAGE_FILES = []
    filename = []

    # Updated image directory path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    imageDir = os.path.join(BASE_DIR, 'seemeehere', 'faces')

    if userImage:
        img_path = os.path.join(imageDir, userImage)

        # Pre-check for image existence
        if not os.path.exists(img_path):
            print(f"File not found: {img_path}")
            return  # Or handle more gracefully depending on your application needs

        # Load and append image if exists
        img = face_recognition.load_image_file(img_path)
        IMAGE_FILES.append(img)
        filename.append(userImage.split(".", 1)[0])

    def encoding_img(IMAGE_FILES):
        encodeList = []
        for img in IMAGE_FILES:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def addAttendance(name):
        with open('attendance.csv', 'r+') as f:
            mypeople_list = f.readlines()
            dateList = []
            now = datetime.now()
            datestring = now.strftime('%m/%d/%Y')
            for line in mypeople_list:
                entry = line.split(',')
                dateList.append(entry[1])
            if datestring not in dateList:
                f.writelines(f'\n{name},{datestring}')

    encodeListKnown = encoding_img(IMAGE_FILES)
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        imgc = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgc = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        facesCurrent = face_recognition.face_locations(imgc)
        encode_facesCurrent = face_recognition.face_encodings(imgc, facesCurrent)

        for encodeFace, faceLoc in zip(encode_facesCurrent, facesCurrent):
            matches_face = face_recognition.compare_faces(encodeListKnown, encodeFace)
            face_distance = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(face_distance)

            if matches_face[matchIndex]:
                name = filename[matchIndex].upper()
                putText = 'Captured'
                y1, x2, y2, x1 = faceLoc

                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 0, 0), cv2.FILLED)
                cv2.putText(img, putText, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                addAttendance(name)  # taking name for attendance function above

        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        key = cv2.waitKey(20)
        if key == 27:
            cap.release()
            cv2.destroyAllWindows()
            break

@app.route('/take_attendance/<userid>')
def take_attendance(userid):
    print(f"Attempting to take attendance for user ID: {userid}")

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE id = %s', (userid, ))
    user = cursor.fetchone()

    if user and user['picture']:
        print(f"User found with picture: {user['picture']}")
        try:
            return Response(generate(user['picture']),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
            return 'Error during face recognition process', 500
    else:
        print("No user picture available or user not found")
        return 'No user picture available or user not found', 404

if __name__ == "__main__":
    app.run(debug=True)
    os.execv(__file__, sys.argv)
