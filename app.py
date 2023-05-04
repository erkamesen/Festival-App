from flask_wtf import CSRFProtect
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from config import Config

from models import Join, Ticket, db

from utils import join_us_form, name_control, mail_control, logger, generate_ticket, get_ticket_image

from iyzico import Iyzico


app = Flask("__name__")
app.config.from_object(Config)
db.init_app(app)




@app.route("/")
def index():
    return render_template("index.html")


@app.route("/bize-katil", methods=["POST"])
def join_us():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        education = request.form.get("flexRadioDefault")
        find_where = request.form.get("flexRadioDefault2")
        experince = request.form.get("flexRadioDefault3")
        join_us_form(name=name, email=email, education=education, find_where=find_where, experience=experince)

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
        datas = Iyzico.create_payment_form(name=name, surname=surname, email=email, ticket_code=ticket_code, price=price)
        conversationId = datas["conversationId"]
        session[conversationId] = {
            "locale":datas["locale"],
            "conversationId":conversationId,
            "token":datas["token"]
        }
        session[f"ticket-{conversationId}"] ={
            "ticket_type":ticket_code,
            "price":price
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
        session.pop(f"ticket-{cookie_ID}", None)
        if session_datas:
            datas = Iyzico.retrieve_form(session_datas) 
            session.pop(cookie_ID, None)

            if datas["status"] == "success" and datas["paymentStatus"] == "SUCCESS":
                logger(control=True, process=datas)
                ticket_no = generate_ticket(ticket_code=ticket_datas["ticket_type"], price=ticket_datas["price"])
                get_ticket_image(ticket_no=ticket_no)
                return render_template("ticket.html", ticket=f"ticket-{ticket_no}.png")
            
            else:
                logger(control=False, process=datas)
                return redirect(url_for("index"))
        
        else:
            return render_template("404.html")







@app.route("/ticket")
def ticket():
    if not request.args.get("ticketNo"):
        flash("Bilet Bulunamadi.")
        return render_template("ticket.html")
    else:
        ticketNo = request.args.get("ticketNo")
        ticket = ticketNo
        return ticket





@app.errorhandler(404)
def bad_request(e):
    return render_template("404.html")





if __name__ == "__main__":
    app.run()
