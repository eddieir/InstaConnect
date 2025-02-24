from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
from flask_bcrypt import Bcrypt
import os
import re
from datetime import timedelta
from bot.insta_bot import InstaBot

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.abspath('instance/insta_connect.sqlite')}"
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_trending_hashtags():
    return ['#love', '#instagood', '#photooftheday', '#fashion', '#beautiful', '#happy', '#cute', '#tbt', '#like4like', '#followme']

def fetch_instagram_analytics(handle):
    return {
        'followers': 12345,
        'following': 678,
        'posts': 234,
        'engagement_rate': '5.6%',
        'average_likes': 456,
        'average_comments': 78
    }

def validate_password(password):
    if len(password) < 8 or len(password) > 20:
        return False
    if not re.search(r'[A-Za-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not validate_password(password):
            flash('Password must be 8-20 characters long, include letters, numbers, and special characters.')
            return redirect(url_for('register'))
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity={'username': user.username}, expires_delta=timedelta(minutes=15))
            response = make_response(redirect(url_for('dashboard')))
            set_access_cookies(response, access_token)
            return response
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    unset_jwt_cookies(response)
    return response

@app.route('/dashboard')
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    return render_template('dashboard.html', user=current_user)

@app.route('/send_message', methods=['GET', 'POST'])
@jwt_required()
def send_message():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        message = request.form['message']
        hashtags = request.form['hashtags'].split(',')

        photo_path = None
        video_path = None

        if 'photo' in request.files and allowed_file(request.files['photo'].filename):
            photo = request.files['photo']
            photo_filename = secure_filename(photo.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
            photo.save(photo_path)

        if 'video' in request.files and allowed_file(request.files['video'].filename):
            video = request.files['video']
            video_filename = secure_filename(video.filename)
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
            video.save(video_path)

        insta_bot = InstaBot(username, password)
        insta_bot.login()
        insta_bot.send_message_to_large_accounts(message, hashtags, photo_path, video_path)
        insta_bot.logout()

        return redirect(url_for('dashboard'))

    return render_template('send_message.html')

@app.route('/increase_reach', methods=['GET', 'POST'])
@jwt_required()
def increase_reach():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashtags = request.form['hashtags'].split(',')
        comment = request.form['comment']
        like_amount = int(request.form['like_amount'])
        follow_amount = int(request.form['follow_amount'])
        comment_amount = int(request.form['comment_amount'])

        insta_bot = InstaBot(username, password)
        insta_bot.login()
        insta_bot.like_posts(hashtags, like_amount)
        insta_bot.follow_users(hashtags, follow_amount)
        insta_bot.comment_on_posts(hashtags, comment, comment_amount)
        insta_bot.logout()

        return redirect(url_for('dashboard'))

    return render_template('increase_reach.html')

@app.route('/trending_hashtags', methods=['GET'])
def trending_hashtags():
    hashtags = get_trending_hashtags()
    return jsonify(hashtags)

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        handle = request.form['handle']
        analytics = fetch_instagram_analytics(handle)
        return render_template('analyze.html', handle=handle, analytics=analytics)
    return render_template('analyze.html')

if __name__ == '__main__':
    if not os.path.exists('instance'):
        os.makedirs('instance')
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5214)