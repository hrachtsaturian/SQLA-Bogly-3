"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User (db.Model):
    def __repr__(self):
        p = self
        return f'User id={p.id}, first_name={p.first_name}, last_name={p.last_name}, image_url={p.image_url}'
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False, unique=True)
    last_name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)

    posts = db.relationship("Post", backref="user")


class Post (db.Model):
    def __repr__(self):
        p = self
        return f'Post id={p.id}, title={p.title}, content={p.content}, createdat={p.created_at} user_id={p.user_id}'
    
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False, unique=True)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class PostTag (db.Model):
    def __repr__(self):
        p = self
        return f'post_id={p.post_id}, tag_id={p.tag_id}'
    
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag (db.Model):
    def __repr__(self):
        p = self
        return f'id={p.id}, name={p.name}'
    
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    posts = db.relationship('Post', secondary='posts_tags', backref='tags')


def connect_db(app):
    db.app = app
    db.init_app(app)