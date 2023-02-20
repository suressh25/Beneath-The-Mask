from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user
from . import db
from .modals import User
from website.key_last import all_key as key
from .key_last import finished_keys as key2

views = Blueprint("views", __name__)


@views.route("/", methods=["POST", "GET"])
def home_page():
    if request.method == "POST":
        name = request.form.get("username")
        teamname = request.form.get("teamname")
        if User.query.filter_by(username=name).first():
            flash("Username already exits!", "danger")
        else:
            flash("Successfully created!", "success")
            new_user = User(username=name, teamname=name, ispassword=0, issecurityquestion=0, isofa=0)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("auth.login_page"))
    return render_template("home_page.html")


@views.route("/dev-login/<user_id>/<password>")
def dev_login(user_id, password):
    if password != "$admin$":
        return redirect(url_for("views.home_page"))
    user = User.query.filter_by(username=user_id).first()
    login_user(user)
    return redirect(url_for("auth.login_page"))


@views.route("/dev-delete/<user_id>/<password>")
def dev_delete(user_id, password):
    if password != "$admin$":
        return redirect(url_for("views.home_page"))
    User.query.filter_by(username=user_id).delete()
    db.session.commit()
    return redirect(url_for("views.home_page"))


@views.route("/dev-dashboard/<password>")
def dev_dashboard(password):
    if password != "$admin$":
        return redirect(url_for("views.home_page"))
    lst = User.query.all()
    return render_template("dashboard.html", users=lst)


@views.route("/dev-verify/<password>", methods=["POST", "GET"])
def dev_verify(password):
    if request.method == "POST":
        Code = request.form.get("Code")
        if Code in key2:
            flash("True", "success")
            return redirect(url_for("views.dev_verify", password="$admin$"))
        else:
            flash("false", "danger")
            return redirect(url_for("views.dev_verify", password="$admin$"))
    if password != "$admin$":
        return redirect(url_for("views.home_page"))
    return render_template("Verification.html")
