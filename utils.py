import qrcode
import time
import os

def generate_qrcode(url):
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,)
    qr.add_data(url)
    qr.make(fit=True)
    code = qrcode.make(url)
    img = qr.make_image(back_color=(255, 195, 235), fill_color=(55, 95, 35))
    


generate_qrcode("http://www.batkarfest.com")