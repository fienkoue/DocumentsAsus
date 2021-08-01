from flask import Flask, render_template,request,redirect,flash,session,logging, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from . import db,app


from models import db,CarsModel,User,UserMixin,LoginManager,generate_password_hash,check_password_hash,current_user,LoginManager,login_user,logout_user,login_required
from forms import LoginForm, RegisterForm






@app.route('/login/', methods=['get'])
def login():
    return render_template('login.html')

@app.route('/signup/', methods=['get'])
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User( name=name,username=username,email=email, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user,remember=remember)
    return redirect(url_for('main.profile'))

   



@app.route('/logout/')
@login_required
def logout():
    logout_user()    
    flash("You have been logged out.")
    return redirect(url_for('main.index2'))

if __name__ == '__main__':
    app.run(debug=True)