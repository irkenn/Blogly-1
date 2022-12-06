from models import User, Post, db
from app import app

# Drop and create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add the users
Alan = User(first_name= 'Alan', last_name='Alda')
Joel = User(first_name = 'Joel', last_name='Burton')
Jane = User(first_name='Jane', last_name='Smith')

# Add them to the session
db.session.add_all([Alan, Joel, Jane])

# # Commit the changes
db.session.commit()

# Add the posts
post1 = Post(title='Post number 1', content='Theres not much to say', user_id=1)

# Add the post to the session
db.session.add(post1)


# Commit the changes
db.session.commit()


