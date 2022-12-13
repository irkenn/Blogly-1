from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy 
from models import db, connect_db, User, Post, Tag, PostTag 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SECRET KEY'] = "There's_no_spoon"
app.config['SECRET_KEY'] = "There's_no_spoon"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


class Commit_and_Delete():
    """Functions for adding, deleting and commiting methods"""
    def session_add_commit(self, user_or_post_or_tag):
        """Adds and commits the passed object to the session"""  
        db.session.add(user_or_post_or_tag)
        db.session.commit()

    def session_delete_commit(self, user_or_post_or_tag):
        """Deletes and commits the object from the session"""  
        db.session.delete(user_or_post_or_tag)
        db.session.commit()


