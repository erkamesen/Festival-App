from flask import Blueprint, request, flash, render_template
from apps.models.models import Ticket
from apps.controller.controller import get_ticket_image


ticket = Blueprint("ticket", __name__, template_folder="../templates", static_folder="../static")


@ticket.route("/ticket")
def ticket_():
    if not request.args.get("ticketNo"):
        flash("Bilet Bulunamadi.")
        return render_template("404.html")
    else:
        ticket_no = request.args.get("ticketNo")
        ticket = Ticket.query.filter_by(ticket_no=ticket_no).first()
        if ticket:
            ticket = get_ticket_image(ticket_no=ticket_no)
            return render_template("ticket.html", ticket=ticket)
        else:
            flash("Bilet Bulunamadi.")
            return render_template("404.html")