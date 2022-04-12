from flask import Blueprint, render_template, request, flash, make_response, redirect, url_for, abort
from flask_login import login_user, current_user, logout_user
from website import db, login_manager
from .models import User
from .forms import LoginForm, SignupForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    # Check to Ensure User isn't Already Logged In
    if current_user.is_authenticated:

        return redirect(url_for('views.profile'))
    
    form = LoginForm()

    # Check to see if the Form has been Submitted
    if form.validate_on_submit():

        # Obtain the Data Passed in the Form to Create the User Logging In
        user = User.query.filter_by(user_email = form.email.data).first()

        # If an Account Exists with that Email Address AND Password is Valid
        if user and user.check_password(password=form.password.data):

            # Login and Validate the 'user'
            # 'user' should be an Instance of the 'User' Class
            login_user(user)

            flash('Login Requested for User {}, Success!'.format(form.email.data))

            return redirect(url_for('views.home'))

        flash('Login Requested - Invalid Email and/or Password Provided!')
        return redirect('/login')

    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    
    # Logout the Current User
    logout_user()

    return redirect(url_for('views.home'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    
    form = SignupForm()

    # Check to see if the Form has been Submitted
    if form.validate_on_submit():

        # Validating that NO User already exists with entered Username and/or Email Address since those Fields are Unique
        #.filter() Returns ALL Records which Match the Given Criteria; .first() Means we are Expecting a Maximum of ONE Record
        existing_user = User.query.filter(User.user_email == form.email.data or User.username == form.username.data).first()

        if existing_user:

            return make_response(f'{form.email.data} and/or {form.username.data} already used on an existing account!')

        # If Username and Email are both Unique then Create an Instance of the User Class
        new_user = User(
            user_email = form.email.data,
            username = form.username.data,
            #user_password = form.password.data,
            user_phone_number = form.phone_number.data,
            user_key_phrases = '',
            user_impairment = form.impairment.data,
            audibleon_role_id = 2
        )

        # Set the Hashed Password for the User
        new_user.set_password(form.password.data)

        # Add the Nuew User to the Database
        db.session.add(new_user)

        # Commit the Changes to the Database
        db.session.commit()

        return redirect('/login')

    return render_template('sign_up.html', form=form)

@login_manager.user_loader
def load_user(user_id):

    # Check if User is Logged-In on Every Page Load
    if user_id is not None:
        
        return User.query.get(user_id)
    
    return None

@login_manager.unauthorized_handler
def unauthorized():

    # Redirect Unauthorized Users to Login Page
    flash('You Must be Logged-In to View that Page.')
    return redirect(url_for('auth.login'))
