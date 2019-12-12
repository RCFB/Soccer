
import flask_login
from flask import request, redirect, render_template, url_for
from wtforms import StringField, PasswordField, IntegerField, validators
from werkzeug.exceptions import Forbidden, InternalServerError
from flask_wtf import FlaskForm
from functools import wraps

from . import app, auth_model

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not flask_login.current_user.admin:
            raise Forbidden
        return func(*args, **kwargs)
    return wrapper

class SignUpForm(FlaskForm):
    email = StringField(label='Email address', validators=[validators.Email()])
    password = PasswordField(label='New password', validators=[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField(label='Repeat password')
 
class SignInForm(FlaskForm):
    email = StringField(label='Email address', validators=[validators.Email()])
    password = PasswordField(label='Password', validators=[validators.DataRequired()])


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm(request.form)
    if request.method != 'POST' or not form.validate():
        return render_template('sign_up.html', form=form)
    # TODO : inscrire l'utilisateur
    email = form.email.data
    password = form.password.data
    user = auth_model.User()
    user.set_email(email)
    user.set_password(password)
    try:
        user.save()
    except Exception :
       return render_template('sign_up.html',
        form=form,
        error='Email already exists.')       
    flask_login.login_user(user)
    return redirect('/')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm(request.form)
    if request.method != 'POST' or not form.validate():
        return render_template('sign_in.html', form=form)
    # TODO : verifier le mot de passe et connecter l'utilisateur
    email = form.email.data
    password = form.password.data
    user = auth_model.find_user_by_email(email)
    if user is None or not user.check_password(password):
        return render_template('sign_in.html', 
                               form=form, 
                               error='Invalid Login or password.')
    flask_login.login_user(user)
    return redirect('/')
    
@app.route('/log_out')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect('/')

@app.route('/users')
#@admin_required
def users():
    users = auth_model.users()
    return render_template('users.html', users=users)