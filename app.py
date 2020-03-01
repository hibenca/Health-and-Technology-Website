from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
db = SQLAlchemy(app)

class BlogPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)


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


@app.route('/<string:user>')
def user(user):
    return f"What up {user}"


if __name__ == '__main__':
    app.run(debug=True)
