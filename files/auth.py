# Importing necessary libraries
from flask import(
    Blueprint, session, 
    request, render_template, 
    flash, redirect ) 

from werkzeug.security import (
    generate_password_hash, check_password_hash )

from files.db_models import(
    Users, Notes, Registration, Login )

from flask_login import(
    login_user, logout_user,
    login_required,
) 

from files import login_manager, db

login_manager.login_message = ''

# Registering the blueprint for the auth route
auth = Blueprint('auth', __name__)

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"%s" % (error), 'error')

@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter(Users.id == int(user_id)).first()


# Here is the code that powers the user registration:
@auth.route('/register', methods = ['GET', 'POST'])
def register():

    # Creating a registration form object:
    form = Registration()

    # Checking the request method and registering user:
    if request.method == "POST":

        # Validating user input using Flask WTF's "validate_on_submit" method
        if form.validate_on_submit():
            

            # Creating a user model to later add it to the database:
            new_user = Users( name = form.data['name'],
                              email = form.data['email'], 
                              password = generate_password_hash( form.data['password']))
            db.session.add(new_user)
            db.session.commit() # Commiting to the db

            # Logging user in using Flask-Login login_manager:
            login_user(new_user)
            return redirect('/')

        # If the data doesn't correspond refresh the register page
        else:
            flash_errors(form)
            return render_template("register.html", form = form)
            

    # If we only just visited the page, then we render it
    elif request.method == "GET":
        return render_template("register.html", form = form)
    

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    login = Login()

    if request.method == "POST":

        if login.validate_on_submit:
            
            if not login.data['email'] or not login.data['password']:
                flash("Please enter your credentials!")
                return render_template("login.html", login = login)

            user = Users.query.filter_by(email = login.data['email']).first()
            if not user:
                flash("User doesn't exist!")
                return render_template("login.html", login = login)
            
            user_password = user.password
            if not check_password_hash(str(user_password), login.data['password']):
                flash("Incorrect password!")
                return render_template("login.html", login = login)

            login_user(user)
            return redirect("/")

    # If we only just entered the login page, just rendering it
    elif request.method == "GET":
        return render_template("login.html", login = login)


# Here we just simply log the user out:
@auth.route('/logout')
@login_required
def logout():

    # Calling the Flask Login "logout_user function to easily logout"
    logout_user()
    return redirect('/login')


    




















    """
            new_user = Users(email = email, password = hashed_password)
            db.session.add(new_user)
            db.session.commit()
    """