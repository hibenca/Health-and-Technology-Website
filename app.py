from flask import Flask, render_template, url_for

app = Flask(__name__)

all_posts = [
    {
        "title": "Post 1",
        "content": "This is my content",
        "author": "Corey"
    },
    {
        "title": "Post 2",
        "content": "This is my content 2"
    }
]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/posts')
def posts():
    return render_template("posts.html", posts=all_posts)

@app.route('/<string:user>')
def user(user):
    return f"What up {user}"


if __name__ == '__main__':
    app.run(debug=True)
