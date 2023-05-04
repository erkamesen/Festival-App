import iyzipay
import os
from dotenv import load_dotenv
import json
import time


load_dotenv()


class Iyzico:
    pricing = {
        "K1": 400,
        "K2": 750,
        "K4": 1400,
        "G1": 150,
        "G2": 270,
        "G4": 500
    }
    APIKEY = os.getenv("IYZICO_API")
    SECRETKEY = os.getenv("IYZICO_SECRET_KEY")
    BASE_URL = os.getenv("IYZICO_BASE_URL")

    options = {
        'api_key': APIKEY,
        'secret_key': SECRETKEY,
        'base_url': BASE_URL
    }
    buyer = {
        'id': 'BY789',
        'name': 'John',
        'surname': 'Doe',
        'email': 'email@email.com',
        'identityNumber': '+905069790202',
        'registrationAddress': 'Aşağı Tokatlı Mah, Düz Sk. Atlantis St',
        'city': 'Karabük',
        'country': 'Turkey',
        'zipCode': '78600'
    }

    address = {
        'contactName': 'Jane Doe',
        'city': 'Karabük',
        'country': 'Turkey',
        'address': 'Aşağı Tokatlı Mah, Düz Sk. Atlantis St',
        'zipCode': '78600'
    }

    basket_items = [
        {
            'id': 'BI103',
            'name': 'Bilet',
            'category1': 'Electronics',
            'itemType': 'VIRTUAL',
            'price': 750
        }
    ]

    request = {
        'locale': 'tr',
        'conversationId': '1683136072',
        'price': 750,
        'paidPrice': 750,
        'currency': 'TRY',
        'basketId': 'B67832',
        'paymentGroup': 'PRODUCT',
        "callbackUrl": "http://127.0.0.1:5000/result",
        "enabledInstallments": ['2', '3', '6', '9'],
        'buyer': buyer,
        'shippingAddress': address,
        'billingAddress': address,
        'basketItems': basket_items,
    }

    @classmethod
    def create_payment_form(cls, name, surname, email, ticket_code, price):
        cls.buyer["name"] = name
        cls.buyer["surname"] = surname
        cls.buyer["email"] = email
        cls.address["contactName"] = f"{name} {surname}"
        cls.basket_items[0]["id"] = ticket_code
        cls.basket_items[0]["price"] = str(price)
        cls.request["conversationId"] = str(round(time.time(), 0)).split(".")[0]
        cls.request["price"] = str(price)
        cls.request["paidPrice"] = str(price)
        checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(cls.request,
                                                                           cls.options)

        return json.loads(checkout_form_initialize.read().decode('utf-8'))
    
    @classmethod
    def retrieve_form(cls, req):

        checkout_form_result = iyzipay.CheckoutForm().retrieve(request=req, options=cls.options)
        return json.loads(checkout_form_result.read().decode('utf-8'))


if __name__ == "__main__":

    checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(
        Iyzico.request, Iyzico.options)

    data = json.loads(checkout_form_initialize.read().decode('utf-8'))
    print(type(data))
    print(data)

