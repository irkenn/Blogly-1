"""Blogly application."""
from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy 
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SECRET KEY'] = "There's_no_spoon"
app.config['SECRET_KEY'] = "There's_no_spoon"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def redirect_to_users():
    return redirect('/users')


@app.route('/users')
def users_page():
    """This will render the homepage"""
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route('/users/new', methods=['GET'])
def user_form():
    """This will handle the form to get a new user"""
    return render_template("user-form.html")


@app.route('/users/new', methods=['POST'])
def new_user_form():
    """This will create a new user """

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def check_user(user_id):
    """This will retrieve information from the selected user and build a page"""

    current_user =  User.query.get_or_404(user_id)

    return render_template('user-page.html', current_user=current_user)

@app.route('/users/<int:user_id>/edit', methods=['GET'])
def show_edit_user(user_id):
    """This function will render a form to change the parameters of the user"""
    current_user = User.query.get(user_id)
    return render_template('user-edit-form.html', current_user=current_user)
    

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """This function will render a form to change the parameters of the user"""

    current_user = User.query.get(user_id)
    current_user.first_name = request.form["first_name"]
    current_user.last_name = request.form["last_name"]
    current_user.image_url = request.form["image_url"]

    db.session.add(current_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """This function will process a POST request and delete the selected user in the database"""
    
    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    return redirect('/users')