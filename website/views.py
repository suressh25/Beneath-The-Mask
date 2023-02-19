from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_user
from .  import db
from .modals import User
views= Blueprint("views",__name__)

@views.route("/",methods=["POST","GET"])
def home_page():
	if request.method =="POST":
		name=request.form.get("username")
		teamname=request.form.get("teamname")
		if User.query.filter_by(username=name).first():
			flash("Username already exits!","danger")
		else:
			flash("Successfully created!","success")
			new_user=User(username=name,teamname=name)
			db.session.add(new_user)
			db.session.commit()
			login_user(new_user)
			return redirect(url_for("auth.login_page"))
	return render_template("home_page.html")