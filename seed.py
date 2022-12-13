from models import User, Post, Tag, PostTag, db
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
post1 = Post(title='First Post', content='Oh, hai.', user_id=2)
post2 = Post(title='Bop', content='This is the content.', user_id=1)
post3 = Post(title='Because everyone deserves a post', content='Just for everyone to have a post', user_id=3)

db.session.add_all([post1, post2, post3])
db.session.commit()

# Add tags to the datavase 
fun = Tag(name='fun')
evenMore = Tag(name='Even More')
bloop = Tag(name='Bloop')
zope = Tag(name='Zope')

db.session.add_all([fun, evenMore, bloop, zope])
db.session.commit()

# Add tags to a post
fun_post1 = PostTag(post_id=1, tag_id=1)
fun_post2 = PostTag(post_id=2, tag_id=1)
fun_post3 = PostTag(post_id=3, tag_id=1)
evenMore_post1 = PostTag(post_id=1, tag_id=2)
bloop_post2 = PostTag(post_id=2, tag_id=3)
zope_post3 = PostTag(post_id=3, tag_id=4)

db.session.add_all([fun_post1, fun_post2, fun_post3, evenMore_post1, bloop_post2, zope_post3])
db.session.commit()






