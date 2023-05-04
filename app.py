from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from config import Config

from models import db

from utils import join_us_form, name_control, mail_control,\
    logger, generate_ticket, get_ticket_image, send_form_infos, contact_us, ticket_control

from iyzico import Iyzico
from mail_sender import MailSender

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask("__name__")
app.config.from_object(Config)
db.init_app(app)

KEY = os.getenv("SMTP_KEY")
SENDER = os.getenv("SMTP_SENDER_MAIL")

mail_sender = MailSender(token=KEY, sender_mail=SENDER)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        message = request.form.get("message")
        contact_us(email=email, message=message)
    return render_template("index.html")


@app.route("/bize-katil", methods=["POST"])
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

        return redirect(url_for("index"))


@app.route("/payment/<code>", methods=["POST"])
def payment(code):
    name = request.form.get("name")
    surname = request.form.get("surname")
    if not name_control(name=name, surname=surname):
        flash("Lutfen Adinizi ve Soyadinizi Dogru Giriniz.")
        return render_template("404.html")

    email = request.form.get("email")
    if not mail_control(email=email):
        flash("Email Adresini Dogru Giriniz!!!")
        return render_template("404.html")

    ticket_code = code
    if not ticket_code:
        flash("-Bilet Kodu Hatasi- Bize Ulas !")
        return render_template("404.html")
    try:
        price = Iyzico.pricing[ticket_code]
        datas = Iyzico.create_payment_form(
            name=name, surname=surname, email=email, ticket_code=ticket_code, price=price)
        conversationId = datas["conversationId"]
        session[conversationId] = {
            "locale": datas["locale"],
            "conversationId": conversationId,
            "token": datas["token"]
        }
        session[f"ticket-{conversationId}"] = {
            "ticket_type": ticket_code,
            "price": price
        }
        session[f"user-{conversationId}"] = {
            "name": f"{name} {surname}",
            "email": email
        }
        resp = make_response(datas["checkoutFormContent"])
        resp.set_cookie("conversationId", conversationId)
        return resp
    except:
        flash("Niye burdasin bir fikrimiz yok 🤷🤷 <br>Bize Ulas !!")
        return render_template("404.html")


@app.route("/result", methods=["POST"])
def result():
    if request.method == "GET":
        return render_template("404.html")
    else:
        cookie_ID = request.cookies.get("conversationId")
        session_datas = session[cookie_ID]
        ticket_datas = session[f"ticket-{cookie_ID}"]
        user_datas = session[f"user-{cookie_ID}"]
        session.pop(f"ticket-{cookie_ID}", None)
        session.pop(f"user-{cookie_ID}", None)
        session.pop(cookie_ID, None)
        if session_datas:
            datas = Iyzico.retrieve_form(session_datas)
            if datas["status"] == "success" and datas["paymentStatus"] == "SUCCESS":
                logger(control=True, process=datas)
                ticket_no = generate_ticket(
                    ticket_code=ticket_datas["ticket_type"], price=ticket_datas["price"])
                mail_sender.send_ticket(receiver=user_datas["email"], name=user_datas["name"],
                                         link=f"http://127.0.0.1:5000/ticket?ticketNo={ticket_no}")
                return redirect(url_for("ticket", ticketNo=ticket_no))

            else:
                logger(control=False, process=datas)
                flash("Bir sorun ile karlsilastik... Tekrar dene veya yardim al.")
                return render_template("404.html")

        else:
            return render_template("404.html")


@app.route("/ticket")
def ticket():
    if not request.args.get("ticketNo"):
        flash("Bilet Bulunamadi.")
        return render_template("ticket.html")
    else:
        ticket_no = request.args.get("ticketNo")
        if ticket_control(ticket_no=ticket_no):
            ticket = get_ticket_image(ticket_no=ticket_no)
            return render_template("ticket.html", ticket=ticket)
        else:
            flash("Bilet Bulunamadi.")
            return render_template("404.html")


@app.errorhandler(404)
def bad_request(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run()
