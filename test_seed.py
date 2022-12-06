from models import User, Post, db
from app import app

# Drop and create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add the users
first = User(first_name='One', last_name='Uno', image_url='Oops')
Alan = User(first_name= 'Alan', last_name='Alda')
Joel = User(first_name = 'Joel', last_name='Burton')
Jane = User(first_name='Jane', last_name='Smith')

# Add them to the session
db.session.add_all([first, Alan, Joel, Jane])

# # Commit the changes
db.session.commit()

# Add the posts
post1 = Post(title='Post number 1', content='Theres not much to say', user_id=1)
post2 = Post(title='Post number 2', content='Theres still not much to say', user_id=2)

# Add the post to the session
db.session.add_all([post1, post2])

# Commit the changes
db.session.commit()