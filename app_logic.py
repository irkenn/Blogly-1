from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy 
from models import db, connect_db, User, Post, Tag, PostTag 
from db_basic_tools import Commit_and_Delete

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SECRET KEY'] = "There's_no_spoon"
app.config['SECRET_KEY'] = "There's_no_spoon"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

blogyToolbox = Commit_and_Delete()

class Blogly_users():
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
        blogyToolbox.session_add_commit(new_user)

    def update_user(self, user_id, request_form):
        current_user = self.get_single_user(user_id)

        """Retrieve values from the request form and place them in the current user"""
        current_user.first_name = request_form["first_name"]
        current_user.last_name = request_form["last_name"]
        current_user.image_url = request_form["image_url"]
        
        """Add and commit"""
        blogyToolbox.session_add_commit(current_user)
    
    def delete_user(self, user_id):
        current_user = self.get_single_user(user_id)
        
        """Delete and commit"""
        blogyToolbox.session_delete_commit(current_user)
    
class Blogly_posts():
    """Functions for creating, deleting and updatings posts"""

    def __init__(self):
        self.blogly_users = Blogly_users()

    def get_single_post(self, post_id):
        """Retrieves a single post from the database using the post ID"""

        return Post.query.get_or_404(post_id)
    
    def create_new_post(self, user_id, request_form):
        """Retrieve from form"""
        post_title = request_form["title"]
        post_content = request_form["content"]

        """Create a post using the model and add & commit"""
        new_post = Post(title=post_title, content=post_content, user_id=user_id)
        blogyToolbox.session_add_commit(new_post)
        
        return self.blogly_users.get_single_user(user_id)

    def edit_post(self, post_id, request_form):
        """Edits the current post"""
        current_post = self.get_single_post(post_id)
        current_post.title = request_form["title"]
        current_post.content = request_form["content"]
        blogyToolbox.session_add_commit(current_post)

        return current_post
    
    def delete_post(self, post_id):
        """Deletes the post"""
        current_post = self.get_single_post(post_id)
        blogyToolbox.session_delete_commit(current_post)
        return current_post        

class Blogly_tags():
    """This contains all the function s"""
    def get_all_tags(self):
        """Returns all the tags in the database"""
        return Tag.query.all()

    def add_tag(self, tag_form):
        """Retrieves the name from the form and add it to the database"""
        new_tag = Tag(name=tag_form['name'])
        blogyToolbox.session_add_commit(new_tag)
    
    def retrieve_single_tag(self, tag_id):
        """This will receive a tag id and return an query object"""
        return Tag.query.get(tag_id)
    
    def delete_tag(self, tag_id):
        """This will retrieve the tag and commit the canges in the database"""
        current_tag = Tag.query.get(tag_id)
        blogyToolbox.session_delete_commit(current_tag)
    
    # def eliminate_tagposts_loop(self, keyword, eliminate_set):
    #     """This will iterate through the set and eliminate all the id 
    #     relations Post-Tag that are listed inside"""
    #     for i in eliminate_set:
    #         PostTag.query.filter(PostTag.{keyword} == i).delete()
    #     db.session.commit()
        
    def dissociate_tags_from_posts(self, tag_id, request_form):
        """This will retrieve the current posts associated with a tag 
        and compare them with the posts that weren't checked in the form
        to eliminate the association from that post with that tag(PostTags)"""
        tag_posts = Tag.query.get(tag_id).posts
        posts_user_list = set()
        posts_db_list = set()

        """Get a set of only the id's from the post associated with that tag"""
        for post in tag_posts:
            posts_db_list.add(post.id)

        """Make a set of only the id's of the request form"""
        for post in request_form:
            if post != 'name':
                posts_user_list.add(int(post[0]))
                
        """Get a set of the posts that don't appear in the request form but 
        do appear in the database and delete the association Post-Tag"""

    #     eliminate_post = posts_db_list - posts_user_list
    #    self.eliminate_tagposts_loop(post_id, eliminate_post) 
        
        eliminate_post = posts_db_list - posts_user_list
        for i in eliminate_post:
            PostTag.query.filter(PostTag.post_id == i).delete()
        db.session.commit()
    
    def dissociate_posts_from_tags(self, post_id, request_form):
        """This is the equivalent to function 'dissociate_tags_from_posts' 
        will retrieve the current tags associated with a posts and compare 
        them with the tags that weren't checked in the form to eliminate 
        the association from that post with that tag"""
        post_tags = Post.query.get(post_id).tags
        tags_user_list = set()
        tags_db_list = set()

        """Get a set of only the id's from the post associated with that tag"""
        for tag in post_tags:
            tags_db_list.add(tag.id)
        
        """Get a set of only the the id's from the request that were selected in the 
        form"""
        for key, value in request_form.items():
            print("value", value[0] == 'on')
            if value[0] == 'on':
                tags_user_list.add(int(key))
        
        """Get a set of the posts that don't appear in the request form but 
        do appear in the database and delete the association Post-Tag"""
        # eliminate_tags = tags_db_list - tags_user_list
        # self.eliminate_tagposts_loop("tag_id", eliminate_tags) 
        
        eliminate_tags = tags_db_list - tags_user_list
        for i in eliminate_tags:
            PostTag.query.filter(PostTag.tag_id == i).delete()
        db.session.commit()

    def actualize_tag_name(self, tag_id, request_form):
        """This will compare if the tag name has changed and update the name in 
        the database if it applies"""
        current_tag = Tag.query.get(tag_id)

        if request_form['name'] != current_tag.name:
            current_tag.name = request_form['name']
            blogyToolbox.session_add_commit(current_tag)
        


        




        





        



        
        

    




    











    






    
    


        

