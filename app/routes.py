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



def send_email(reciever_mail):
    """Script that enables sending of email"""
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "testgheebee@gmail.com"  # Enter your address
    receiver_email = "sobowalegz2@gmail.com"  # Enter receiver address
    #password = getpass.getpass("Type your password and press enter: ")
    password = "vudj vaqu wbfn biaw"  #this is the passoword i used to test the code. it can be replaced with the company credentials.
    subject = "Welcome to Momech Auto Services"

      # HTML content of the email
    html_content = """
    <html>
    <body>
        <h1>Welcome to Momech Auto Services!</h1>
        <p>Thanks for registering with Momech.</p>
        <p>If you encounter issues, feel free to reach out to us.</p>
    </body>
    </html>
    """

    message = f"""\
    Subject: {subject}
    MIME-Version: 1.0
    Content-Type: text/html
    {html_content}
    """
   
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send mail: {e}")
    
@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        print("User is already authenticated, redirecting to home page")
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        print("Form submitted and valid")
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()

        send_email(user.email) 

        flash('Your account has been created! You can Login Now', 'success')
        print("Flash message displayed")
        return redirect(url_for('main.login'))
    else:
        print("Form not submitted or not valid")
        print("Form data:", form.data)
        print(form.errors) 

    print("Rendering registration form")
    return render_template('registration_form.html', title='Register', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    print("Login route triggered.")
    if current_user.is_authenticated:
        print("User is already authenticated.")
        return redirect(url_for('main.account'))
    
    form = Login()
    if form.validate_on_submit():
        print("Form submitted.")
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password_hash.encode('utf-8')):
            print("Login successful.")
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            print("Next page:", next_page)
            return redirect(next_page) if next_page else redirect(url_for('main.account'))
        else:
            print("Login unsuccessful. Invalid email or password.")
            flash('Login Unsuccessful. Please check email and password', 'danger')
    else:
        print("Form not submitted or validation failed.")

    return render_template('login_form.html', title='Login', form=form)

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


@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/service')
def service():
    return render_template('service.html')

@main.route('/location')
def location():
    return render_template('location.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/account')
@login_required
def account():
    service_form = ServiceRequestForm()
    if service_form.validate_on_submit():
        service_request = ServiceRequestForm(
            user_id=current_user.id,
            service_type=service_form.service_type.data,
            description=service_form.description.data,
            location=service_form.location.data
        )
        db.session.add(service_request)
        db.session.commit()
        flash('Service request submitted!', 'success')
        return redirect(url_for('main.account'))

    #service_requests = ServiceRequestForm.query.filter_by(user_id=current_user.id).all()
    feedbacks = Feedback.query.filter_by(user_id=current_user.id).all()

    return render_template(
        'account.html', 
        title='Account Dashboard', 
        service_form=service_form, 
        #service_requests=service_requests,
        feedbacks=feedbacks
    )