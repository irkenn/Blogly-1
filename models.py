from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import Computed


db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)


"""Models for Blogly."""

class User(db.Model):
  """This is the user model"""
  __tablename__ = 'users'

  def __repr__(self):
    p = self
    return f"<User id={p.id} first_name={p.first_name} last_name={p.last_name} image_url={p.image_url}>"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  
  first_name = db.Column(db.String(50), nullable=False)
  
  last_name = db.Column(db.String(50), nullable=False)
  
  image_url = db.Column(db.String, default="https://img.wattpad.com/8f19b412f2223afe4288ed0904120a48b7a38ce1/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f5650722d38464e2d744a515349673d3d2d3234323931353831302e313434336539633161633764383437652e6a7067")

  posts = db.relationship('Post', backref='posts', passive_deletes=True)
  # posts = db.relationship('Post', backref='posts', cascade='all,delete' )


class Post(db.Model):
  """This is the model for posts"""
  __tablename__ = 'posts'

  def __repr__(self):
    p = self
    return f"<Post id={p.id} title={p.title} created_at={p.created_at} user_id={p.user_id}>"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

  title = db.Column(db.String(50), nullable=False)

  content = db.Column(db.String(300), nullable=False)

  created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

  # users = db.relationship('User', backref='users', passive_deletes=True)



