from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required

from app.models import User
from app.forms import LoginForm, RegistrationForm
from app.services import UserService

bp: Blueprint = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user_service: UserService = UserService()
        data: dict = {
            "username": form.username.data,
            "email": form.email.data,
            "password": form.password.data,
        }
        user = user_service.create_user(data)
        login_user(user)
        flash("Registration successful. You are logged in.", "success")
        return redirect(url_for("main.index"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.authenticate(form.user_id.data, form.password.data)
        if user is not None:
            login_user(user)
            flash("Login successful.", "success")
            return redirect(url_for("main.index"))
        flash("Wrong user ID or password.", "danger")
    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "info")
    return redirect(url_for("main.index"))
