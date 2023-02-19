from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import login_required,logout_user
auth=Blueprint("auth",__name__)

@auth.route("/login/",methods=["POST,GET"])
def login_page():
	if request.method=="POST":
		if request.form.get("username")=="bruh" and request.form.get("password") =="bruh@123":
			flash("password_correct")

	return render_template("login.html")
@auth.route("/test/")
@login_required
def test():
	return "<h2>This is test page</h2>"

@auth.route("/logout/")
@login_required
def logout():
	logout_user()
	return redirect(url_for("views.home_page"))