import requests



def qr_code(id):
    r = requests.get(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={id}")
    return r



