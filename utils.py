import qrcode
import time  # for filename.
import os  # for delete qrcode images after create a new ticket
from PIL import Image  # for merging images
import secrets

from models import Join, Ticket, db


""" Generate QRCODE """


def generate_qrcode(url):
    """
    Generates a qrcode for the link given as a parameter.
    Returns the name of the image file as the value for deletion of
    the file after the ticket is created.
    """

    filename = str(time.time())
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(back_color=(255, 195, 235), fill_color=(55, 95, 35))
    img.save(f"./assets/{filename}.jpg")
    return filename


""" Generate TICKET IMAGE """


def generate_ticket_image(url):

    file = generate_qrcode(url)
    img = Image.open("./assets/ticket.jpg")
    img.paste(Image.open(
        f"./assets/{file}.jpg").resize((1500, 1500)), (3750, 170))
    img.save(f"./assets/ticket-{file}.png")
    # TICKET CREATED
    os.chdir("./assets")
    os.remove(f"{file}.jpg")
    os.chdir("../")
    # QRCODE FILE DELETED
    return f"ticket-{file}.png"


""" Generate TICKET """


def generate_ticket(ticket_type, price):
    while True:
        ticket_no = secrets.token_hex(16)
        if Ticket.query.filter_by(ticket_no=ticket_no).first():
            continue
        else:
            break

    new_ticket = Ticket(ticket_no=ticket_no, ticket_type=ticket_type, price=price)
    db.session.add(new_ticket)
    db.session.commit()
    url = f"http://127.0.0.1:5000/ticket/{ticket_no}"


""" FORM """


def join_us_form(name, email, education, find_where, experience):
    new_member = Join(name=name,
                      email=email,
                      education=education,
                      find_where=find_where,
                      experience=experience
                      )
    db.session.add(new_member)
    db.session.commit()


if __name__ == "__main__":
    pass
