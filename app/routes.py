from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user,login_required
from app.models import User
from app.models import waisay_wali_query,my_query
from werkzeug.urls import url_parse
from app import db


@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('home.html', title='Flask App')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Incorrect username/password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registered')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/waisay_wali_query')
def merry_query():
    return str(waisay_wali_query())

@app.route('/my_query/<int:id>')
def my__query(id):
    return (my_query(id).username)

app.config["IMAGE_UPLOADS"] = 'app\static\img\uploads'
app.config["ALLOWED_IMG_EXTENSIONS"]=["PNG","JPG","JPEG"]
@app.route("/upload-image", methods=["GET","POST"]) 
def upload_image():

    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            if image.filename == "":
                return redirect(request.url)
            if not allowed_imgs(image.filename):
                print("invalid image")
                return redirect(request.url)
            

            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            print(image)
            return redirect(request.url)



    return render_template('upload_image.html',title='image')

    def allowed_imgs(filename):
        if not "." in filename:
            return False
        ext = filename.rsplit(".",1)[1]
        if ext.upper() in app.config["ALLOWED_IMG_EXTENSIONS"]:
            return True
        else:
            return False