from flask_sqlalchemy import SQLAlchemy
import time

db = SQLAlchemy()

class Join(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    education = db.Column(db.String)
    find_where = db.Column(db.String)
    experience = db.Column(db.String)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ticket_no = db.Column(db.String)
    ticket_Type = db.Column(db.String)
    price = db.Column(db.Integer)
    created_time = db.Column(db.String, default=time.time())




