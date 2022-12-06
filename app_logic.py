from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy 
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SECRET KEY'] = "There's_no_spoon"
app.config['SECRET_KEY'] = "There's_no_spoon"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

class Blogly():

    """Functions for adding, deleting and commiting methods"""
    def session_add_commit(self, user_or_post):
        """Adds and commits the passed object to the session"""  
        db.session.add(user_or_post)
        db.session.commit()

    def session_delete_commit(self, user_or_post):
        """Deletes and commits the object from the session"""  
        db.session.delete(user_or_post)
        db.session.commit()

    """ Functions for retrieving single or multiple users"""
    def get_all_users(self):
        """Returns all the current users in the database"""
        
        return User.query.all()

    def get_single_user(self, user_id):
        """Retrieve a single user from the database based on its ID"""

        return User.query.get(user_id)

    def get_single_user_or_404(self, user_id):
        """Will retrieve a single user from the database, based on its ID"""

        return User.query.get_or_404(user_id)
    
    """Functions for creating, deleting and updating users"""
    def create_new_user(self, request_form):
        """Retrieve values from the request formt"""
        first_name = request_form["first_name"]
        last_name = request_form["last_name"]
        image_url = request_form["image_url"]
        
        """Will create a new user using User class model"""
        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        
        """ Add and commmit it to the database using built in class method"""
        self.session_add_commit(new_user)

    def update_user(self, user_id, request_form):
        current_user = self.get_single_user(user_id)

        """Retrieve values from the request form and place them in the current user"""
        current_user.first_name = request_form["first_name"]
        current_user.last_name = request_form["last_name"]
        current_user.image_url = request_form["image_url"]
        
        """Add and commit"""
        self.session_add_commit(current_user)
    
    def delete_user(self, user_id):
        current_user = self.get_single_user(user_id)
        
        """Delete and commit"""
        self.session_delete_commit(current_user)
    
    """Functions for creating, deleting and updatings posts"""
    def get_single_post(self, post_id):
        """Retrieves a single post from the database using the post ID"""

        return Post.query.get_or_404(post_id)
    
    def create_new_post(self, user_id, request_form):
        """Retrieve from form"""
        post_title = request_form["title"]
        post_content = request_form["content"]

        """Create a post using the model and add & commit"""
        new_post = Post(title=post_title, content=post_content, user_id=user_id)
        self.session_add_commit(new_post)
        
        return self.get_single_user(user_id)

    def edit_post(self, post_id, request_form):
        """Edits the current post"""
        current_post = self.get_single_post(post_id)
        current_post.title = request_form["title"]
        current_post.content = request_form["content"]
        self.session_add_commit(current_post)

        return current_post
    
    def delete_post(self, post_id):
        """Deletes the post"""
        current_post = self.get_single_post(post_id)
        self.session_delete_commit(current_post)
        return current_post        













    






    
    


        

