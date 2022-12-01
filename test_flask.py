from unittest import TestCase

from app import app
from models import db, User


# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for the view functions used in User"""

    def setUp(self):
        """Add a new user"""

        User.query.delete()

        new_user = User(first_name='One', last_name='Uno', image_url='Oops')
        db.session.add(new_user)
        db.session.commit()

        self.user = new_user

    def tearDown(self):
        """Clean any fouled transaction"""

        db.session.rollback()
    


    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Two", "last_name": "Dos", "image_url": "Wee"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Dos", html)          

    def test_home_page(self):
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(self.user.first_name, html)

    def test_redirect_home_page(self):
        with app.test_client() as client:
            response = client.get('/', follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('One', html)
    
    def test_user_id(self):
        with app.test_client() as client:
            response = client.get(f'/users/{self.user.id}')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(self.user.first_name, html)            
