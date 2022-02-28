from flask import Blueprint, render_template, request, flash

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