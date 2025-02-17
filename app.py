from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from bot.insta_bot import InstaBot

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/insta_connect.sqlite'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "insta_connect.sqlite")}'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if 'user_id' not in session:
        return redirect(url_for('login'))
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
def increase_reach():
    if 'user_id' not in session:
        return redirect(url_for('login'))
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

if __name__ == '__main__':
    if not os.path.exists('instance'):
        os.makedirs('instance')
    with app.app_context():
        db.create_all()
    app.run(debug=True)