import qrcode
import os  # for delete qrcode images after create a new ticket
from PIL import Image  # for merging images
import secrets
from email_validator import validate_email, EmailNotValidError
from apps.pkg.telegram import Logger
from dotenv import load_dotenv
from apps.models.models import Team, Ticket, db
from io import BytesIO


load_dotenv()

TELEGRAM_APIKey = os.getenv("TELEGRAM_APIKey")
TELEGRAM_chatID = os.getenv("TELEGRAM_chatID")
telegram_logger = Logger(token=TELEGRAM_APIKey, chat_id=TELEGRAM_chatID)


""" Generate QRCODE """


def generate_qrcode(url):
    """
    Generates a qrcode for the link given as a parameter.
    Returns the buffer with created qrcode
    """

    buffer = BytesIO()
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,)
    qr.add_data(url)
    f = qr.make(fit=True)
    img = qr.make_image(back_color=(255, 195, 235), fill_color=(55, 95, 35))
    img.save(buffer)
    buffer.seek(0)
    return buffer


def get_ticket_image(ticket_no):
    """ 
    It takes the values of ticketNo query strings coming to the /ticket endpoint as a parameter.
    If there is an image file in assets, it returns the filename directly,
    otherwise it renders and returns it. 
    """
    if os.path.exists(f"./apps/static/assets/ticket-{ticket_no}.png"):
        return f"ticket-{ticket_no}.png"
    else:
        file = generate_qrcode(
            f"http://127.0.0.1:5000/ticket?ticketNo={ticket_no}")
        img = Image.open("./apps/static/assets/ticket.jpg")
        img.paste(Image.open(
            file).resize((1500, 1500)), (3750, 170))
        img.save(f"./apps/static/assets/ticket-{ticket_no}.png", quality=30)
        return f"ticket-{ticket_no}.png"


""" Generate TICKET """


def generate_ticket(ticket_type, price):
    """
    It takes the type and price of the ticket as parameters.
    It checks the database with a while loop and generates code until a unique code is received.
    Return ticket_code = ticket_no
    """

    while True:
        ticket_no = secrets.token_hex(8)
        if Ticket.query.filter_by(ticket_no=ticket_no).first():
            continue
        else:
            break

    new_ticket = Ticket(ticket_no=ticket_no,
                        ticket_type=ticket_type, price=price)
    db.session.add(new_ticket)
    db.session.commit()
    return ticket_no


""" FORM """


def join_us_form(name, email, education, find_where, experience):
    """ 
    It receives the data of the post requests from the
    /bize-katil endpoint and processes it into the Team table. """
    new_member = Team(name=name,
                      email=email,
                      education=education,
                      find_where=find_where,
                      experience=experience
                      )
    db.session.add(new_member)
    db.session.commit()


def send_form_infos(name, email, education, find_where, experience):
    """
    It receives the data of the post requests from the
    /bize-katil endpoint and send them to specified chatId with Telegram Bot.
    """
    telegram_logger.info(f"Aramiza Katilmak isteyen birisi var:\nAd: {name}\nEmail: {email}\nEgitim Durumu: {education}\
                         \nBizi nerden Buldu ?: {find_where}\nDeneyim: {experience}")


def name_control(name, surname):
    """
    It is used to handle browser-based name and surname errors in the purchase process.
    """
    if not name or not surname:
        return False
    if len(name) > 30 or len(surname) > 25:
        return False
    else:
        return True


def mail_control(email):
    """
    It is used to check the correctness of the email with the email_validator.
    Return True-False
    """
    if not email:
        return False
    try:
        v = validate_email(email)
        email = v["email"]
        return True
    except EmailNotValidError:
        return False


def payment_logger(state, process):
    """
    Used to log purchase success or failure.
    The information is stored in the form of json.
    """
    with open(f"{state}.log", "a") as f:
        f.write(f"{process}\n")


def contact_us(email, message):
    """ 
    It receives the post request information from the contact us form
    in the index and sends it to chatId via telegram.
    """
    telegram_logger.info(f"Yeni bir mesajimiz var:\n\
Email:{email}\nMesaj:{message}")
