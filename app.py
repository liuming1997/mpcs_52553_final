import os
from flask import Flask, session, request, redirect, render_template, g, flash, url_for
import json
import sqlite3

app = Flask(__name__)

users = [];

@app.before_request
def before_request_check():
    if not session.get('id'):
        # Visitor is unknown, return to login
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['pass']
        if username in users and password == users[user].password:
            session['user'] = username;
            return(redirect(url_for('dashboard')))
    return render_template("login.html")  

@app.route('/')
def index():
    return render_template("dashboard.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/settings')
def settings():
    return render_template("settings.html") 

@app.route('/logout')
def logout():
    return render_template("login.html")


# course routes
@app.route('/courses/home')
def courses():
    return render_template("courses/home.html")

@app.route('/courses/announcements')
def course_announcements():
    return render_template("courses/announcements.html")

@app.route('/courses/announcements_view')
def view_assignment():
    return render_template("courses/announcements_view.html")

@app.route('/courses/assignments')
def course_assignments():
    return render_template("courses/assignments.html")

@app.route('/courses/grades')
def course_grades():
    return render_template("courses/grades.html")

@app.route('/courses/home')
def course_home():
    return render_template("courses/home.html")

@app.route('/courses/modules')
def course_modules():
    return render_template("courses/modules.html")

@app.route('/courses/syllabus')
def course_syllabus():
    return render_template("courses/syllabus.html")

@app.route('/courses/<course>')
def course_syllabus():
    return render_template("courses/course.html", course_name=course_name, assignments=assignments, announcements=announcements)


# IGNORE FOR NOW. Just pulling in some authorization management stuff from my other project



# @app.route('/')
# def index():
#     if not session.get('uuid'):
#         # Visitor is unknown, give random ID
#         session['uuid'] = str(uuid.uuid4())
#     return render_template("index.html")


# @app.route('/login', methods=["GET", "POST"])
# def login():
#     global CLIENT_ID
#     global CLIENT_SECRET
#     global REDIRECT_URI
#     global scope

#     # Pull authorization manager from Spotify
#     auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope,
#                                                 cache_path=session_cache_path(), 
#                                                 show_dialog=True)

#     session['auth_manager'] = auth_manager

#     if request.args.get("code"):
#         # Being redirected from Spotify auth page
#         auth_manager.get_access_token(request.args.get("code"))
#         return redirect('/generate_festival')

#     if not auth_manager.get_cached_token():
#         # Display sign in link when no token is found
#         auth_url = auth_manager.get_authorize_url()
#         return redirect(auth_url)
#     else:
#         return redirect('/generate_festival')

