from flask import Blueprint, redirect, render_template, request, session, flash, make_response, url_for
from apps.controller.controller import name_control, mail_control, generate_ticket, payment_logger
from apps.pkg.iyzico import Iyzico
from apps.pkg.mail_sender import MailSender
import os
from dotenv import load_dotenv


load_dotenv()

KEY = os.getenv("SMTP_KEY")
SENDER = os.getenv("SMTP_SENDER_MAIL")
mail_sender = MailSender(token=KEY, sender_mail=SENDER)



payment = Blueprint("payment", __name__, template_folder="../templates", static_folder="../static")



@payment.route("/payment/<code>", methods=["POST"])
def payment_(code):
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
        conversationId = datas.get("conversationId")
        session[conversationId] = {
            "locale": datas.get("locale"),
            "conversationId": conversationId,
            "token": datas.get("token")
        }
        session[f"ticket-{conversationId}"] = {
            "ticket_type": ticket_code,
            "price": price
        }
        session[f"user-{conversationId}"] = {
            "name": f"{name} {surname}",
            "email": email
        }
        resp = make_response(datas.get("checkoutFormContent"))
        resp.set_cookie("conversationId", conversationId)
        return resp
    except:
        flash("Niye burdasin bir fikrimiz yok 🤷🤷 <br>Bize Ulas !!")
        return render_template("404.html")


@payment.route("/result", methods=["POST"])
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
            if datas.get("status") == "success" and datas.get("paymentStatus") == "SUCCESS":
                payment_logger(control="successful", process=datas)
                ticket_no = generate_ticket(
                    ticket_code=ticket_datas.get("ticket_type"), price=ticket_datas.get("price"))
                mail_sender.send_ticket(receiver=user_datas.get("email"), name=user_datas.get("name"),
                                        link=f"http://127.0.0.1:5000/ticket?ticketNo={ticket_no}")
                return redirect(url_for("ticket.ticket_", ticketNo=ticket_no))

            else:
                error_code = datas.get("errorCode", "10000")
                error_message = datas.get("errorMessage", "Bir sorun ile karlsilastik... Tekrar dene veya yardim al.")
                flash(f"{error_code}-{error_message}")
                payment_logger(control="failure", process=datas)
                return render_template("404.html")

        else:
            return render_template("404.html")




