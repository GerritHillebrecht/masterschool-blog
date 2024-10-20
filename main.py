from uuid import uuid4
from flask import Flask, request, render_template, redirect, url_for

from storage import read_from_file, write_to_file

app = Flask(__name__)


@app.route('/')
def index():
    blog_posts = read_from_file()
    return render_template('index.html', posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def route_post_add():
    print("method", request.method)
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        content = request.form.get("content")

        if not title or not author or not content:
            print("missing data")
            return render_template("add.html")

        blog_posts = read_from_file()
        blog_posts.append({
            "id": str(uuid4()),
            "title": title,
            "author": author,
            "content": content,
        })
        write_to_file(blog_posts)

        return redirect(url_for('index'))

    return render_template("add.html")


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
