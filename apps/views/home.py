from flask import Blueprint, request, render_template, redirect, url_for
from apps.controller.controller import join_us_form, send_form_infos, contact_us


home = Blueprint("home", __name__, template_folder="../templates", static_folder="../static")


@home.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        message = request.form.get("message")
        contact_us(email=email, message=message)
        return redirect(url_for("home.index"))
    else:
        return render_template("index.html")


@home.route("/bize-katil", methods=["POST"])
def join_us():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        education = request.form.get("education")
        find_where = request.form.get("find_where")
        experience = request.form.get("experience")
        join_us_form(name=name, email=email, education=education,
                    find_where=find_where, experience=experience)
            
        send_form_infos(name=name, email=email, education=education,
                    find_where=find_where, experience=experience)

        return redirect(url_for("home.index"))
    else:
        return render_template("404.html")