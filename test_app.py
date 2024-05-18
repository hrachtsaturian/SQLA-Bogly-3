from unittest import TestCase

from app import app
from models import db, User, Post
import datetime

app.config['TESTING'] = True



class BloglyTestCase(TestCase):

    def setUp(self):
        with app.app_context():
            db.create_all()
            new_user = User(id=123, first_name='Max', last_name='Mad', image_url='image.png')
            new_post = Post(id=23, title='First', content='Surprise', user_id=123)
            db.session.add(new_user)
            db.session.add(new_post)
            db.session.commit()


    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Max', html)

    def test_show_add_form(self):
        with app.test_client() as client:
            resp = client.get('/users/new')

            self.assertEqual(resp.status_code, 200)
    

    def test_show_user_detail(self):
        with app.test_client() as client:
            resp = client.get('/users/123')

            self.assertEqual(resp.status_code, 200)

    def test_show_user_edit_form(self):
        with app.test_client() as client:
            resp = client.get('/users/123/edit')

            self.assertEqual(resp.status_code, 200)

# II

    def test_show_post_form(self):
        with app.test_client() as client:
            resp = client.get('/users/123/posts/new')

            self.assertEqual(resp.status_code, 200)

    def test_show_post_detail(self):
        with app.test_client() as client:
            resp = client.get('/posts/23')

            self.assertEqual(resp.status_code, 200)

    

