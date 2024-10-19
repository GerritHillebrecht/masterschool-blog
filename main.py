from flask import Flask, render_template
from storage import read_from_file

app = Flask(__name__)


@app.route('/')
def index():
    blog_posts = read_from_file()
    return render_template('index.html', posts=blog_posts)


@app.route("/post/<int:post_id>")
def route_post_id(post_id: int):
    blog_posts = read_from_file()
    blog_post = next(
        blog_post
        for blog_post in blog_posts
        if blog_post.get("id") == post_id
    )

    return render_template("blog-post.html", post=blog_post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
