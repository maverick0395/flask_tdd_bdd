from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_required

from app.forms import PublishPostForm, UpdatePostForm
from app.logger import log
from app.models import Post
from app.services import PostService

bp: Blueprint = Blueprint("posts", __name__, url_prefix="/posts")


@bp.route("/all", methods=["GET"])
@login_required
def get_all_posts():
    if not current_user.is_authenticated:
        return redirect(url_for("auth/login"))
    post_service: PostService = PostService()
    posts = post_service.get_all()
    return render_template("posts/post-list.html", posts=posts)


@bp.route("/my_posts", methods=["GET"])
def get_all_user_posts():
    post_service: PostService = PostService()
    posts = post_service.get_all_by_filter_query(user_id=current_user.id)
    return render_template("posts/post-list.html", posts=posts)


@bp.route("/<int:pk>", methods=["GET"])
def get_post_by_id(pk):
    post_service: PostService = PostService()
    post = post_service.get(id=pk)
    return render_template("posts/post-info.html", post=query)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    """Creating new post"""

    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    post_service: PostService = PostService()
    form = PublishPostForm(request.form)
    if form.validate_on_submit():
        data: dict = {
            "title": form.title.data,
            "body": form.body.data,
            "user_id": current_user.id,
        }
        post_service.create_post(data)
        flash("Post has been created")
        return redirect(url_for("posts.get_all_posts"))
    elif form.is_submitted():
        for error in form.errors:
            for msg in form.errors[error]:
                log(log.ERROR, "create_post(): %s", msg)
                flash(msg, "warning")
    return render_template("posts/create.html", form=form)


@bp.route("/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    post_service: PostService = PostService()
    post: Post = post_service.get(id=post_id)
    form = UpdatePostForm(obj=post)
    if form.validate_on_submit():
        data: dict = {"title": form.title.data, "body": form.body.data}
        post_service.update_post(id=post_id, **data)
        return redirect(url_for("posts.get_all_posts"))
    return render_template("posts/update.html", form=form)


@bp.route("/<int:post_id>/delete", methods=["GET", "DELETE"])
@login_required
def delete_post(post_id):
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    post_service: PostService = PostService()
    post = post_service.get(id=post_id)
    if post is not None:
        post_service.delete(id=post_id)
        return redirect(url_for("posts.get_all_posts"))
    return render_template("404.html"), 404
