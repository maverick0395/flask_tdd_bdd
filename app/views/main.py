from flask import redirect, render_template, Blueprint, url_for
from flask_login import current_user, login_required

bp: Blueprint = Blueprint("main", __name__)


@bp.route("/")
@login_required
def index():
    if current_user.is_authenticated:
        return render_template("index.html")
    return redirect(url_for("auth.login"))
