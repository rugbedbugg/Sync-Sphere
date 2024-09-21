from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, flash
from werkzeug.utils import secure_filename
import os
import json
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = 'we gonna crack devjams'  # For session management

users = {}      # we can store it in a database a get it in a json file format and then convert it


# Configuration for file uploads
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Pre-home page route
@app.route('/')
def pre_home():
    if 'user' in session:
        return render_template('pre_home.html')
    else:
        return redirect(url_for('login'))

# Route to log out
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['user'] = username                                                              # Store user in session
            flash('Login successful!', 'success')
            return redirect(url_for('pre_home'))
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html')


def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash('Username already exists. Please choose another.', 'danger')
        else:
            users[username] = password                                                              # Add new user to our "database"
            flash('Account created successfully. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')


# Home page
@app.route('/home')
def home():
    return render_template('home.html')

# Image to PDF converter page
@app.route('/image_to_pdf', methods=['GET', 'POST'])
def image_to_pdf():
    if request.method == 'POST':
        files = request.files.getlist('images')
        pdf = FPDF()
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                pdf.add_page()
                pdf.image(os.path.join(app.config['UPLOAD_FOLDER'], filename), 10, 10, 180, 240)
        
        output_pdf = "output.pdf"
        pdf.output(os.path.join(app.config['UPLOAD_FOLDER'], output_pdf))
        return send_from_directory(app.config['UPLOAD_FOLDER'], output_pdf, as_attachment=True)
    
    return render_template('image_to_pdf.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Statistics page
@app.route('/statistics')
def statistics():
    # Example: study hours for each day of the week (replace with actual data from your database)
    study_hours = [3, 2, 4, 5, 6, 1, 0]  # Monday to Sunday

    return render_template('statistics.html', study_hours=study_hours)

# YouTube video catalogue
@app.route('/learning')
def learning(video_id):
    return render_template('learning.html', video_id=video_id)

@app.route('/watch_video/<video_id>')
def watch_video(video_id):
    return render_template('watch_video.html', video_id=video_id)

if __name__ == '__main__':
    app.run(debug=True)



