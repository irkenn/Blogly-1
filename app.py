"""Blogly application."""
from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy 
from models import db, connect_db, User, Post
from app_logic import Blogly

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SECRET KEY'] = "There's_no_spoon"
app.config['SECRET_KEY'] = "There's_no_spoon"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
blogly = Blogly()

"""Routes related to the users only"""
@app.route('/')
def redirect_to_users():
    """Redirect to /users """
    
    return redirect('/users')

@app.route('/users')
def users_page():
    """This will render the homepage"""
    users = blogly.get_all_users()
    
    return render_template("users.html", users=users)

@app.route('/users/new', methods=['GET'])
def user_form():
    """This will handle the form to get a new user"""
    
    return render_template("user-form.html")

@app.route('/users/new', methods=['POST'])
def new_user_form():
    """This will pass the request form to and add a new user to the database using Blogly class method"""
    blogly.create_new_user(request.form)
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def check_user(user_id):
    """This will retrieve information from the selected user and build a page"""
    current_user =  blogly.get_single_user_or_404(user_id)

    return render_template('user-page.html', current_user=current_user)

@app.route('/users/<int:user_id>/edit', methods=['GET'])
def show_edit_user(user_id):
    """This will render a form to change the parameters of the user"""
    current_user = blogly.get_single_user(user_id)

    return render_template('user-edit-form.html', current_user=current_user)
    
@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """This function will receive the new parameters and add them to the database"""    
    blogly.update_user(user_id, request.form)

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """This function will process a POST request and delete the selected user in the database"""
    blogly.delete_user(user_id)
    
    return redirect('/users')

"""Routes related to posts from the users"""
@app.route('/users/<int:user_id>/posts/new')
def get_post_form(user_id):
    """Will process a GET request and render the HTML post form, for user to fill"""
    current_user = blogly.get_single_user(user_id)
    
    return render_template('post-form.html', current_user=current_user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def include_new_post(user_id):
    """Will incorporate the new post by the user to the database"""    
    current_user = blogly.create_new_post(user_id, request.form)

    return render_template('user-page.html', current_user=current_user)

@app.route('/posts/<int:post_id>')
def send_post_detail_form(post_id):
    """This will extract the selected post from the database and pass it through"""
    current_post = blogly.get_single_post(post_id)
    current_user = blogly.get_single_user(current_post.user_id)

    return render_template('post-detail.html', current_post=current_post, current_user=current_user)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form_get_route(post_id):
    """Will send a form to the user to modify the current post"""
    current_post = blogly.get_single_post(post_id)
    
    return render_template('post-edit.html', current_post=current_post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post_form_post_method(post_id):
    """Will incorporate the edited post to the database"""
    current_post = blogly.edit_post(post_id, request.form)

    return redirect(f'/users/{current_post.user_id}')
    # return render_template('post-detail.html', current_post=current_post)

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Will delete the selected post from the database and will redirect to the user page"""
    current_post = blogly.delete_post(post_id)
    
    return redirect(f'/users/{current_post.user_id}')