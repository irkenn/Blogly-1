from models import User, db
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
db.session.add(Alan)
db.session.add(Joel)
db.session.add(Jane)

# Commit the changes
db.session.commit()


