from uuid import uuid4

from flask import Flask, request, render_template, redirect, url_for
from slugify import slugify

from storage import read_from_file, write_to_file

app = Flask(__name__)

DEFAULT_IMAGE = "https://plus.unsplash.com/premium_photo-1678900924337-51991a683ab1?q=80&w=1740&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"


# READ
@app.get('/')
def index():
    blog_posts = read_from_file()
    return render_template('index.html', posts=blog_posts)


@app.get("/post/<string:post_slug>")
def route_post_id(post_slug: str):
    blog_posts = read_from_file()
    blog_post = next(
        blog_post
        for blog_post in blog_posts
        if blog_post.get("slug") == post_slug
    )

    return render_template("blog-post.html", post=blog_post)


# CREATE
@app.get("/add")
def route_post_add():
    return render_template("add.html")


@app.post("/add")
def route_post_add_template():
    title = request.form.get("title")
    author = request.form.get("author")
    content = request.form.get("content")

    if not title or not author or not content:
        print("missing data")
        return render_template("add.html")

    blog_posts = read_from_file()
    blog_posts.append({
        "uuid": str(uuid4()),
        "slug": slugify(title),
        "title": title,
        "author": author,
        "content": content,
        "image": DEFAULT_IMAGE
    })
    write_to_file(blog_posts)

    return redirect(url_for('index'))


# UPDATE
@app.get("/update/<string:post_uuid>")
def route_update_post_template(post_uuid):
    posts = read_from_file()
    print("seached uuid", post_uuid)
    for p in posts:
        print("uuid", p.get("uuid"))
    post = next(
        p
        for p in posts
        if p.get("uuid") == post_uuid
    )
    print("looked up post:", post)
    return render_template("update.html", post=post)


@app.post("/update/<string:post_uuid>")
def route_update_post(post_uuid):
    print(f"Updating {post_uuid}")

    existing_post = next(
        post
        for post in read_from_file()
        if post.get("uuid") == post_uuid
    )

    print("Existing post: ", existing_post)

    author = request.form.get("author") or existing_post.get("author", "Unknown")
    title = request.form.get("title") or existing_post.get("title", "No title given")
    slug = slugify(title)
    content = request.form.get("content") or existing_post.get("content", "Empty blog post")
    image = request.form.get("image") or existing_post.get("image", DEFAULT_IMAGE)

    post = {
        "uuid": post_uuid,
        "author": author,
        "title": title,
        "slug": slug,
        "content": content,
        "image": image,
    }

    print("What the fuck?", post)

    updated_posts = list(
        post
        for post in read_from_file()
        if post.get("uuid") != post_uuid
    )

    print("updated posts?", updated_posts)

    updated_posts.append(post)
    write_to_file(updated_posts)

    return redirect(url_for('index'))


# DELETE
@app.get("/delete/<string:post_uuid>")
def route_delete_post(post_uuid):
    blog_posts = list(
        blog_post
        for blog_post in read_from_file()
        if blog_post.get("uuid") != post_uuid
    )
    write_to_file(blog_posts)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
