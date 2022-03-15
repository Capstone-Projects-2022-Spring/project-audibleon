from flask import Blueprint, render_template, request, flash, make_response, redirect, url_for, abort
from flask_login import login_user, current_user, logout_user
from website import db, login_manager
from .models import User
from .forms import LoginForm, SignupForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", text="testing", user = "tim", boolean = True)

@auth.route('/logout')
def logout():
    
    # Logout the Current User
    logout_user()

    return redirect(url_for('views.home'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        data = request.form
        print(data)

        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        ## basically create error checking here to make sure that the user information is valid
        if len(email) < 4:
           flash('Email address must be at least 4 characters', category='error')
        elif len(username) < 2:
            flash('Username must be at least 2 characters', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        else:
            flash('Account created! :)', category='success')
            ## add the user information to the database
    return render_template("sign_up.html")

@auth.route('/register', methods=['GET', 'POST'])
def register():

    username = request.args.get('user')
    email = request.args.get('email')

    if username and email:

        # Validating that NO User already exists with entered Username and/or Email Address since those Fields are Unique
        #.filter() Returns ALL Records which Match the Given Criteria; .first() Means we are Expecting a Maximum of ONE Record
        existing_user = User.query.filter(User.username == username or User.user_email == email).first()

        if existing_user:

            return make_response(f'{username} and/or {email} already used on an existing account!')

        # If Username and Email are both Unique then Create an Instance of the User Class
        new_user = User(
            user_email = email,
            username = username,
            user_password = 'test123',
            user_phone_number = '(111)-111-1111',
            user_key_phrases = '',
            user_impairment = 1,
            audibleon_role_id = 2
        )

        # Add the New User to the Database
        db.session.add(new_user)

        # Commit the Changes to the Database
        db.session.commit()

        # Redirect to the Sign-Up Page
        redirect(url_for('auth.register'))

    # Return a List of the Existing User Profiles
    return render_template('profile_list.html', users=User.query.all(), title='Profiles List')

@auth.route('/sign-in', methods=['GET', 'POST'])
def sign_in():

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

            return redirect(url_for('views.profile'))

        flash('Login Requested - Invalid Email and/or Password Provided!')
        return redirect('/sign-in')

    return render_template('signin.html', form=form)

@auth.route('/reg', methods=['GET', 'POST'])
def reg():

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

        return redirect('/sign-in')

    return render_template('register.html', form=form)

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
    return redirect(url_for('auth.sign_in'))
