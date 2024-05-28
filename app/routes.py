"""Module that contains the routes"""
import getpass
import smtplib, ssl
import bcrypt
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Feedback, Mechanic, Driver
from app.forms import RegistrationForm, FeedbackForm, ServiceRequestForm
from app.forms import Login

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()

        send_email(user.email) #function that sends confirmation male to new users

        flash('Your account has been created! You can Login Now', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)


def send_email(reciever_mail):
    """Script that enables sending of email"""
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "testgheebee@gmail.com"  # Enter your address
    receiver_email = "sobowalegz2@gmail.com"  # Enter receiver address
    #password = getpass.getpass("Type your password and press enter: ")
    password = "vudj vaqu wbfn biaw"  #this is the passoword i used to test the code. it can be replaced with the company credentials.
    subject = "Welcome to Momech Auto Services"
    body = "Thanks for registering with Momech \n If you encounter issue, reach out to us."

    message = f"""\
    Subject: {subject}

    {body}
    """

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send mail: {e}")
        





@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password_hash.encode('utf-8')):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(name=form.name.data, email=form.email.data, rating=form.rating.data, comments=form.comments.data, user_id=current_user.id)
        db.session.add(feedback)
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('main.home'))
    return render_template('feedback.html', title='Feedback', form=form)

@main.route('/service_request', methods=['GET', 'POST'])
@login_required
def service_request():
    if current_user.role != 'driver':
        flash('Only drivers can request services.', 'danger')
        return redirect(url_for('main.home'))
    form = ServiceRequestForm()
    if form.validate_on_submit():
        #implement google api here to find mechanics available in a given area
        flash('Your service request has been submitted.', 'success')
        return redirect(url_for('main.home'))
    return render_template('service_request.html', title='Service Request', form=form)


#function that enables user to send recieve email notification.
