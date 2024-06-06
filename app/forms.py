#!/usr/bin/env python3
"""
Module that implements the forms feature of the application
"""
from flask_wtf import FlaskForm
from wtforms.validators import (
        DataRequired, Length, Email, EqualTo, Regexp
        )
from wtforms import SubmitField, StringField, PasswordField, BooleanField, TextAreaField, IntegerField, SelectField, FloatField
from wtforms.validators import NumberRange, InputRequired


class RegistrationForm(FlaskForm):
    """Class that handles the registration task for new users"""
    username = StringField(
            "Username",
            validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField(
        "Surname",
        validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField(
        "First Name",
        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone Number", validators=[Regexp('^\+(?:[0-9] ?){6,14}[0-9]$')])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
            "Confirm Password",
            validators=[DataRequired(), EqualTo("password")])
    role = SelectField("Role", choices=[('driver', 'Driver'), ('mechanic', 'Mechanic')], validators=[DataRequired()])
    vehicle_details = StringField("Vehicle Details")  #for drivers
    location = StringField("Location")  # for mechanics
    expertise = StringField("Expertise")  #for mechanics
    service_rates = FloatField("Service Rates")  #for mechanics
    submit = SubmitField("Sign Up")


class Login(FlaskForm):
    """class that handles the login task of user"""
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")

class FeedbackForm(FlaskForm):
    """Class that handles responses gotten as feedback after a service has been rendered"""
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[DataRequired(), Length(min=6, max=120)])
    rating = IntegerField("Rating (1-5)", validators=[DataRequired(), NumberRange(min=1, max=5)])
    comments = TextAreaField("Comments", validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField("Submit Feedback")

class ServiceRequestForm(FlaskForm):
    """Class that handles the service requests """
    service_type = StringField('Service Type', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Request Service')