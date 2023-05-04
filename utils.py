import qrcode
import time  # for filename.
import os  # for delete qrcode images after create a new ticket
from PIL import Image  # for merging images
import secrets
from email_validator import validate_email, EmailNotValidError
from telegram import Logger
from dotenv import load_dotenv
from models import Join, Ticket, db


load_dotenv()

TELEGRAM_APIKey = os.getenv("TELEGRAM_APIKey")
TELEGRAM_chatID = os.getenv("TELEGRAM_chatID")
telegram_logger = Logger(token=TELEGRAM_APIKey, chat_id=TELEGRAM_chatID)
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
    img.save(f"./static/assets/{filename}.jpg")
    return filename


""" Generate TICKET IMAGE """


def get_ticket_image(ticket_no):
    if os.path.exists(f"./static/assets/ticket-{ticket_no}.png"):
        return f"ticket-{ticket_no}.png"
    else:
        file = generate_qrcode(
            f"http://127.0.0.1:5000/ticket?ticketNo={ticket_no}")
        img = Image.open("./static/assets/ticket.jpg")
        img.paste(Image.open(
            f"./static/assets/{file}.jpg").resize((1500, 1500)), (3750, 170))
        img.save(f"./static/assets/ticket-{ticket_no}.png", quality=30)
        # TICKET CREATED
        os.chdir("./static/assets")
        os.remove(f"{file}.jpg")
        os.chdir("../")
        os.chdir("../")

        # QRCODE FILE DELETED
        return f"ticket-{ticket_no}.png"


""" Generate TICKET """


def generate_ticket(ticket_code, price):
    while True:
        ticket_no = secrets.token_hex(8)
        if Ticket.query.filter_by(ticket_no=ticket_no).first():
            continue
        else:
            break

    new_ticket = Ticket(ticket_no=ticket_no,
                        ticket_type=ticket_code, price=price)
    db.session.add(new_ticket)
    db.session.commit()
    return ticket_no

def ticket_control(ticket_no):
    if Ticket.query.filter_by(ticket_no=ticket_no).first():
        return True
    else:
        return False



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


def send_form_infos(name, email, education, find_where, experience):

    telegram_logger.info(f"Aramiza Katilmak isteyen birisi var:\nAd: {name}\nEmail: {email}\nEgitim Durumu: {education}\
                         \nBizi nerden Buldu ?: {find_where}\nDeneyim: {experience}")


def name_control(name, surname):
    if not name or not surname:
        return False
    if len(name) > 30 or len(surname) > 25:
        return False
    else:
        return True


def mail_control(email):
    if not email:
        return False
    try:
        v = validate_email(email)
        email = v["email"]
        return True
    except EmailNotValidError:
        return False


def logger(control, process):
    if control:
        with open("./logs/succesful.log", "a") as f:
            f.write(f"{process}\n")
    else:
        with open("./logs/failure.log", "a") as f:
            f.write(f"{process}\n")



def contact_us(email, message):
    telegram_logger.info(f"Yeni bir mesajimiz var:\n\
Email:{email}\nMesaj:{message}")

if __name__ == "__main__":
    pass
