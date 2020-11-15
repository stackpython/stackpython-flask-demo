"""
A simple website yet complete features e.g. CRUD, login, 
logout, form, etc using Flask (Python web framework)
by Sonny STACKPYTHON
"""


from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

from covid import covid_obj

import random
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required ,UserMixin, login_user, logout_user, current_user
from form import LoginForm  


# Create a flask app, and use SQLite as a simple database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Hardcode to secret key for development only
# You can use a related library to generate secret-key automatically
app.config['SECRET_KEY'] = "your-secret-key-here"

# Login manager for flask-login
login_manager = LoginManager() 
login_manager.login_view = 'login' 
login_manager.init_app(app)


# Inherit all necessary methods from UserMixin class
class User(UserMixin, db.Model):
    """Create columns to store our data"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    # Create a method to verify hashed password to 
    # authenticate a user from a form(Login form)
    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    # A Python special method used to display an object 
    # to be easy to read
    def __repr__(self):
        return '<User %r>' % self.username


class Course(db.Model):
    """Create this course table to store course details"""

    id = db.Column(db.Integer,
                    primary_key=True)
    title = db.Column(db.String(120),
                      nullable=False)
    description = db.Column(db.Text,
                            nullable=False)
    price = db.Column(db.Integer,
                      nullable=False)
    duration = db.Column(db.Integer,
                         nullable=False)
    instructor = db.Column(db.String(80),
                           nullable=False)
    date_created = db.Column(db.DateTime(),
                             default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


# Only test for first time building a homepage
@app.route('/test')
def home_test():

    name = "Son"
    return render_template("home-test.html", name=name)  


# About page
@app.route('/about')
def about():
    return render_template("about.html")

# Test writing JavaScript inside HTML
@app.route('/script')
def test_script():
    return render_template("test-script.html")


# Show covid-19 information in s single table
@app.route('/covid-table')
def covid_table():
    """Return covid19 data to show in a table"""

    # Assign a new variable 
    # covid_obj is a variable holding data data from covid.py
    covid_data = covid_obj

    return render_template("covid-table.html", covid_data=covid_data)


@app.route('/covid-dashboard')
def covid_dashboard():
    """Return covid19 data to display in a dashboard"""

    # import "covid_obj" data from covid.py
    # then assign it to a new variable "data"
    data = covid_obj

    confirmed_case = data["Confirmed"]
    recovered_case = data["Recovered"]
    hospitalized_case = data["Hospitalized"]
    new_deaths_case = data["NewDeaths"]
    new_confirmed_case = data["NewConfirmed"]
    last_updated = data["UpdateDate"]

    return render_template("covid-dashboard.html", confirmed_case=confirmed_case,
                                                    recovered_case=recovered_case,
                                                    hospitalized_case=hospitalized_case,
                                                    new_deaths_case=new_deaths_case,
                                                    new_confirmed_case=new_confirmed_case,
                                                    last_updated=last_updated)


# Random menu app
@app.route('/random-menu')
def random_menu():
    """This is a random menu app you want to choose a menu randomly
    If this matches a menu you want you have to go to eat it"""

    # Create a random list
    random_list = ["กะเพราหมู", "ไข่เจียวหมูสับ", "หมูทอดกระเทียม", "ก๋วยเตี๋ยว", "ผัดซีอิ๊ว"]

    # Create a variable to hold a random menu in a random list
    menu_data = random.choice(random_list)

    return render_template("random-menu.html", menu_data=menu_data)


@app.route('/create',methods=["GET", "POST"])
@login_required
def create():
    """Create a new course"""

    # Check if method that being sent is "POST"
    if request.method == "POST":

        # Create variables to get input attributes from form
        title = request.form["title"]
        instructor = request.form["instructor"]
        price = request.form["price"]
        duration = request.form["duration"]
        description = request.form["description"]

        # Create an object, then pass variables into the class(Course)
        obj = Course(title=title,
                     instructor=instructor,
                     price=price,
                     duration=duration,
                     description=description)

        # Add the object to SQlAlchemy session
        # then submit it into our database
        db.session.add(obj)
        db.session.commit()

        # Redirect to homepage after submitting form
        return redirect(url_for('home'))
                
    return render_template("create-course.html")


# This is our homepage
@app.route('/')
def home():
    """Retrieve all courses from the database"""

    all_courses = Course.query.all()

    return render_template("home.html", all_courses=all_courses) 


# Course(post) details page
@app.route('/post-details/<int:id>')
@login_required
def post_details(id):
    """Retrieve only one course(by id)"""

    # Query only one course using get "query.get() method"
    single_course = Course.query.get(id)

    return render_template("post-details.html", single_course=single_course)


@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    """Update an existing post(course)"""

    data = Course.query.get(id)

    # Check if method that being sent is "POST"
    if request.method == "POST":

        # Create variables to get input attributes from form
        title = request.form["title"]
        instructor = request.form["instructor"]
        price = request.form["price"]
        duration = request.form["duration"]
        description = request.form["description"]

        data.title = title
        data.instructor = instructor
        data.price = price
        data.duration = duration
        data.description = description

        # Submit an updated post into the database
        db.session.commit()

        # Redirect to home page after finishing update
        return redirect(url_for('home'))

    return render_template('update.html', data=data)


@app.route('/delete/<int:id>', methods=["GET", "POST"])
def delete(id):
    """Delete a post"""

    data = Course.query.get(id)

    db.session.delete(data)
    db.session.commit()

    return redirect(url_for('home'))


@app.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    """Sign up user account"""

    # Check if method that being sent is "POST"
    if request.method == "POST":

        # Create variables to get input attribute values from the form
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        # Create an object, then pass variables 
        # into the User class
        obj = User(username=username, 
                   password=generate_password_hash(password, method='sha256'),
                   email=email)

        # Add an object to SQLAlchemy session
        # then submit into our database
        db.session.add(obj)
        db.session.commit()

        # Redirect to home page after submitting form
        return redirect(url_for('login'))

    return render_template('sign-up.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login function for logging in"""

    # Create an object called "form" to use LoginForm class
    form = LoginForm()
    username = form.username.data
    password = form.password.data

    # Validate a form submitted by a user
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        
        # Check and compare a user's password 
        # in a database, if True, log a user in
        if user and user.verify_password(password):

            # Log a user in after completing verifying a password
            # then flash a message "Successful Login"
            login_user(user)
            flash("Successful Login", "success")
            
            # Redirect to homepage
            return redirect(url_for('home')) 

        else:
            flash("Invalid Login", "danger")
    else:
        # You can print or return something such as an error message
        # In this case, do nothing. But you can do it later
        pass

    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    """# Logout function for logging out"""

    logout_user()
    return redirect(url_for('login'))

# Run our app
# if you are in production, do not use "debug=True"
# Use "debug=False" instead
if __name__ =="__main__":
    app.run(debug=True)
