from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class BlogPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)


class ContactMe(db.Model):
    # MANUAL TABLE NAME
    __tablename__ = "ContactMe"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(10), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __init__(self, name, email, subject, message):
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message

    def __repr__(self):
        return "Contacted Me"


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/posts', methods=["GET", "POST"])
def posts():
    if request.method == "POST":
        post_title = request.form['title']
        post_author = request.form['author']
        post_content = request.form['content']
        new_post = BlogPosts(title=post_title, author=post_author, content=post_content)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/posts")
    else:
        all_posts = BlogPosts.query.all()
        return render_template("posts.html", posts=all_posts)


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPosts.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/posts")


@app.route('/posts/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    post = BlogPosts.query.get(id)

    if request.method == "POST":
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template("/edit.html", post=post)


@app.route('/posts/new', methods=["GET", "POST"])
def new_posts():
    if request.method == "POST":
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        new_post = BlogPosts(title=post_title, author=post_author, content=post_content)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template("new_posts.html")


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/skills')
def skills():
    return render_template('skills.html')


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        contact_message = ContactMe(name, email, subject, message)
        db.session.add(contact_message)
        db.session.commit()
        return redirect('/contact')

    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
