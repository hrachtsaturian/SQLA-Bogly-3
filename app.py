"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, PostTag, Tag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'ihaveasecret'


debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()

# **GET */ :*** Redirect to list of users. (We’ll fix this in a later step).
@app.route('/')
def home():
    return redirect('/users')

# **GET */users :*** Show all users. Make these links to view the detail page for the user. Have a link here to the add-user form.
@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)


# **GET */users/new :*** Show an add form for users
@app.route('/users/new')
def show_add_form():
    return render_template('user_form.html')


# **POST */users/new :*** Process the add form, adding a new user and going back to ***/users***
@app.route('/users/new', methods=['POST'])
def add_new_user():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_url = request.form.get('image_url')

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


# **GET */users/[user-id] :***Show information about the given user. Have a button to get to their edit page, and to delete the user.
@app.route('/users/<int:user_id>')
def show_user_detail(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)


# **GET */users/[user-id]/edit :*** Show the edit page for a user. Have a cancel button that returns to the detail page for a user, and a save button that updates the user.
@app.route('/users/<int:user_id>/edit')
def show_user_edit_form(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('user_edit.html', user=user)


# **POST */users/[user-id]/edit :***Process the edit form, returning the user to the ***/users*** page.
@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_url = request.form.get('image_url')

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


# **POST */users/[user-id]/delete :*** Delete the user.
@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


# II


# **GET */users/[user-id]/posts/new :*** Show form to add a post for that user.
@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('post_form.html', user=user, tags=tags)


# **POST */users/[user-id]/posts/new :*** Handle add form; add post and redirect to the user detail page.
@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
    user = User.query.get_or_404(user_id)
    title = request.form.get('title')
    content = request.form.get('content')
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=title, content=content, user_id=user.id, tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


# **GET */posts/[post-id] :*** Show a post. Show buttons to edit and delete the post.
@app.route('/posts/<int:post_id>')
def show_post_detail(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('post_detail.html', post=post)


# **GET */posts/[post-id]/edit :*** Show form to edit a post, and to cancel (back to user page).
@app.route('/posts/<int:post_id>/edit')
def show_post_edit_form(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('post_edit.html', post=post, tags=tags)


# **POST */posts/[post-id]/edit :*** Handle editing of a post. Redirect back to the post view.
@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    title = request.form.get('title')
    content = request.form.get('content')
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    

    post.title = title
    post.content = content
    post.tags = tags

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')


# **POST */posts/[post-id]/delete :*** Delete the post.
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')


# III


# **GET */tags :*** Lists all tags, with links to the tag detail page.
@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


# **GET */tags/[tag-id] :*** Show detail about a tag. Have links to edit form and to delete.
@app.route('/tags/<int:tag_id>')
def show_tag_detail(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_detail.html', tag=tag)


# **GET */tags/new :*** Shows a form to add a new tag.
@app.route('/tags/new')
def show_tag_form():
    return render_template('tag_form.html')


# **POST */tags/new :*** Process add form, adds tag, and redirect to tag list.
@app.route('/tags/new', methods=['POST'])
def add_new_tag():
    name = request.form.get('name')

    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')


# **GET */tags/[tag-id]/edit :*** Show edit form for a tag.
@app.route('/tags/<int:tag_id>/edit')
def show_tag_edit_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag_edit.html', tag=tag)


# **POST */tags/[tag-id]/edit :*** Process edit form, edit tag, and redirects to the tags list.
@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    name = request.form.get('name')

    tag.name = name

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

# **POST */tags/[tag-id]/delete :*** Delete a tag.
@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')







