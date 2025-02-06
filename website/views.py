from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user
from . import db
from .modals import User

views = Blueprint("views", __name__)
key = "$lapassion$"
home = "views.home_page"


@views.route("/", methods=["POST", "GET"])
def home_page():
    if request.method == "POST":
        name = request.form.get("username")
        collegename = request.form.get("teamname")
        if User.query.filter_by(username=name).first():
            flash("Username already exits!", "error")
        else:
            flash("Successfully created!", "success")
            new_user = User(
                username=name,
                teamname=collegename,
                ispassword=0,
                issecurityquestion=0,
                isofa=0,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("auth.login_page"))
    return render_template("home_page.html")


@views.route("/dev-login/<user_id>/<password>")
def dev_login(user_id, password):
    if password != key:
        return redirect(url_for(home))
    user = User.query.filter_by(username=user_id).first()
    login_user(user)
    return redirect(url_for("auth.login_page"))


@views.route("/dev-delete/<user_id>/<password>")
def dev_delete(user_id, password):
    if password != key:
        return redirect(url_for(home))
    User.query.filter_by(username=user_id).delete()
    db.session.commit()
    return redirect(url_for(home))


@views.route("/dev-dashboard/<password>")
def dev_dashboard(password):
    if password != key:
        return redirect(url_for(home))
    lst = User.query.all()
    return render_template("dashboard.html", users=lst)
