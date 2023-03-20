from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user
from . import db
import pyotp
import datetime

auth = Blueprint("auth", __name__)


@auth.route("/login/", methods=["POST", "GET"])
@login_required
def login_page():
    if request.method == "POST":
        if request.form.get("username") == "bruh" and request.form.get("password") == "bruh@123":
            flash("password_correct", "success")
            current_user.ispassword = True
            current_user.passwordtime = datetime.datetime.now()
            db.session.commit()
            return redirect(url_for("auth.security"))
        return redirect(url_for("auth.login_page"))
    return render_template("login.html")


@auth.route("/security/", methods=["POST", "GET"])
@login_required
def security():
    if request.method == "POST":
        creds = {"Catname": "ALEX", "Hometown": "MADURAI", "Food": "PIZZA"}
        Catname = request.form.get("Catname")
        Hometown = request.form.get("Hometown")
        Food = request.form.get("Food")
        if Catname.upper() == creds["Catname"] and Hometown.upper() == creds["Hometown"] and Food.upper() == creds[
                "Food"]:
            flash("you have answered the security question correctly", "success")
            current_user.issecurityquestion = True
            current_user.securitytime = datetime.datetime.now()
            db.session.commit()
            return redirect(url_for("auth.twofactor"))
        else:
            flash("Wrong Credentials", "danger")
            return redirect(url_for("auth.security"))
    if current_user.ispassword == 0:
        flash("Not authorized", "danger")
        return redirect(url_for("auth.login_page"))
    return render_template("login_security.html")


@auth.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home_page"))


@auth.route("/last_page/")
@login_required
def last_page():
    if current_user.isofa == 0:
        flash("Not authorized", "danger")
        return redirect(url_for("auth.security"))
    return render_template("last_page.html")


@auth.route("/twofactor", methods=["POST", "GET"])
@login_required
def twofactor():
    if request.method == "POST":
        otp = int(request.form.get("otp"))
        if pyotp.TOTP("HHYZTDZOINOAS35RUOTCSIGXV35VEIV2").verify(otp):
            current_user.isofa = True
            db.session.commit()
            flash("The TOTP 2FA token is valid", "success")
            current_user.completed = datetime.datetime.now()
            db.session.commit()
            return redirect(url_for("auth.last_page"))
        else:
            flash("You have supplied an invalid 2FA token!", "danger")
            return redirect(url_for("auth.twofactor"))
    if current_user.issecurityquestion == 0:
        flash("Not authorized", "danger")
        return redirect(url_for("auth.security"))
    return render_template("login_2fa.html")
