from flask import  render_template,url_for,flash , redirect , request 
from m24 import app , db , bcrypt
from flask_wtf import FlaskForm ,Form
from wtforms import SubmitField
from m24.forms import RegistrationForm,  LoginForm , PostForm , AnonymousForm , UploadForm , ContactForm , uploadVideoForm
from m24.models import User , Post , Anonymous , Gallery , my_table , videolink
from flask_login import login_user, current_user , logout_user , login_required
from flask_wtf.file import FileField
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import socket
import base64
import sqlite3
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'Kemparty9@gmail.com'
app.config['MAIL_PASSWORD'] = 'sundarchor'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

s = URLSafeTimedSerializer('Thisisasecret!')


@app.route("/blog")
def blog():
    posts = Post.query.all()
    anonymous = Anonymous.query.all()
    return render_template('home.html', posts=posts,anonymous=anonymous)

@app.route("/play")
def play():
    anonymous = Anonymous.query.all()
    return render_template('play.html', anonymous=anonymous)

@app.route("/new")
def newz():
    return render_template('new.html')
@app.route("/")
@app.route("/work")
def mainnn():
    return render_template('work.html')

@app.route("/gallery")
def gallery():
    
    gallery = my_table.query.all()
    # print(gallery[1].image)
    # with open(gallery[1].image,"rb") as f:
    #     data = f.read()
    # data = base64.b64encode(gallery[0].data)
    # data = data.decode("UTF-8")
    # print(data , "hello")

    return render_template('gallery.html' , gallery=gallery)

@app.route("/video")
def video():
    gall = videolink.query.all()
    # print(gallery[1].image)
    # with open(gallery[1].image,"rb") as f:
    #     data = f.read()
    # data = base64.b64encode(gallery[0].data)
    # data = data.decode("UTF-8")
    # print(data , "hello")

    return render_template('video.html', gall=gall)


@app.route("/about" )
def about():
    return render_template('about.html', title='About' )


@app.route("/mission" )
def mission():
    return render_template('mission.html', title='mission' )


@app.route("/Vision" )
def Vision():
    return render_template('Vision.html', title='Vision' )

@app.route("/Elevator's Pitch" )
def ElevatorsPitch():
    return render_template('ElevatorsPitch.html', title='ElevatorsPitch' )


@app.route("/problem" )
def problem():
    return render_template('problem.html', title='problem' )




@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():

        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data  
        fmail = 'rcraina@gmail.com'
        token = s.dumps(email, salt='email')
        msg = Message('email is sent by  -- ' + str(name) + 'and his mail id is - ' + str(email), sender='Kemparty9@gmail.com', recipients=[fmail])
        msg.body = 'subject  -- ' + str(subject)   + '  CONTENT  --  ' + str(message)
        mail.send(msg)
        return redirect(url_for('contact'))
    return render_template('contact.html', title='contact',form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('gallery'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('mainnn'))



@app.route("/account")
@login_required
def account():
    return render_template('account.html')



@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # 
        file_name = form.file.data
        data = file_name
        if file_name != None :
            data = base64.b64encode(file_name.read())
            data = data.decode("UTF-8")

        # 
        post = Post(title=form.title.data, content=form.content.data, author=current_user , image=data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('blog'))
    return render_template('create_post.html',form=form)


@app.route("/anonymous", methods=['GET', 'POST'])
@login_required
def anonymous_post():
    form = AnonymousForm()
    if form.validate_on_submit():
        anonymous = Anonymous(title=form.title.data, content=form.content.data)
        db.session.add(anonymous)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for("home"))    
    return render_template('lalu.html',form=form)



@app.route('/download', methods=["GET", "POST"])
def download():

    form = UploadForm()

    if request.method == "POST":

        conn= sqlite3.connect("YTD.db")
        cursor = conn.cursor()
        print("IN DATABASE FUNCTION ")
        c = cursor.execute(""" SELECT * FROM  my_table """)

        for x in c.fetchall():
            name_v=x[0]
            data_v=x[1]
            break

        conn.commit()
        cursor.close()
        conn.close()

        return send_file(BytesIO(data_v), attachment_filename='flask.pdf', as_attachment=True)


    return render_template("uploadFile.html", form=form)



@app.route("/uploadFile", methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if request.method == "POST":

        if form.validate_on_submit():
            file_name = form.file.data
            data = base64.b64encode(file_name.read())
            data = data.decode("UTF-8")
            print(data , "hello")
            database(name=file_name.filename, data=file_name.read() , vall = data )
            return render_template("uploadFile.html", form=form)
    return render_template('uploadFile.html', form=form)




def database(name, data , vall):
    conn= sqlite3.connect("m24/site.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS my_table (name TEXT,data BLOP , vall TEXT) """)
    cursor.execute("""INSERT INTO my_table (name, data , vall) VALUES (?,?,?) """,(name,data,vall))

    conn.commit()
    cursor.close()
    conn.close()

@app.route("/uploadVideo", methods=['GET', 'POST'])
def uploadVideo():
    form = uploadVideoForm()
    if form.validate_on_submit():
        txtt = form.link.data
        x = txtt.split("youtu.be/")
        linkk = videolink(link=x[1])
        db.session.add(linkk)
        db.session.commit()
        return render_template("account.html")
    return render_template('uploadVideo.html',form=form)



@app.route("/gallery/<image_name>", methods=['POST'])
@login_required
def delete_image(image_name):
    image = my_table.query.get(image_name)
    db.session.delete(image)
    db.session.commit()
    return redirect(url_for('gallery'))

@app.route("/video/<video_link>", methods=['POST'])
@login_required
def delete_link(video_link):
    video = videolink.query.get(video_link)
    db.session.delete(video)
    db.session.commit()
    return redirect(url_for('video'))

@app.route("/delete/<post_id>", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog'))

