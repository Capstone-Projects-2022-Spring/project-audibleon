from flask import Blueprint, render_template, request, flash, make_response, redirect, url_for
from website import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", text="testing", user = "tim", boolean = True)

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

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


