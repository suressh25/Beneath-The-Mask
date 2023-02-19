from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import login_required,logout_user,current_user
from . import db
auth=Blueprint("auth",__name__)

@auth.route("/login/",methods=["POST","GET"])
@login_required
def login_page():
	if request.method=="POST":
		if request.form.get("username")=="bruh" and request.form.get("password") =="bruh@123":
			flash("password_correct","success")
			current_user.ispassword=True
			db.session.commit()
			return redirect(url_for("auth.test"))
		return redirect(url_for("auth.login_page"))
	return render_template("login.html")


@auth.route("/test/",methods=["POST","GET"])
@login_required
def test():
	if current_user.ispassword==0:
		flash("Not authorized","danger")
		return redirect(url_for("auth.login_page"))
	return "<h2>This is test</h2>"



@auth.route("/logout/")
@login_required
def logout():
	logout_user()
	return redirect(url_for("views.home_page"))