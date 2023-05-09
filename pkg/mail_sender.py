from smtplib import SMTP
import os
from dotenv import load_dotenv


load_dotenv()





KEY = os.getenv("SMTP_KEY")
SENDER = os.getenv("SMTP_SENDER_MAIL")

class MailSender:
    
    def __init__(self, token, sender_mail, 
                 mail_server="smtp.gmail.com", port=587):
        
        self.token = token
        self.sender_mail = sender_mail
        self.mail_server = mail_server
        self.port = port

    def send_ticket(self, receiver, name, link):
        try:
            with SMTP(self.mail_server, self.port) as connection:  
                connection.starttls()  
                connection.login(self.sender_mail, password=self.token)  
                connection.sendmail(from_addr=self.sender_mail,
                                                to_addrs=receiver,
                                                msg=f"Subject:Bilet!\n\nSevgili {name} seni aramizda gormekten cok mutluyuz !\n\
Biletin hazir lutfen asagidaki linke tiklayip biletine hemen kavus !!!\n\n{link}")
        except:
            with open("unsend_mails.txt", "a") as f:
                f.write(f"{receiver} mailini alamadi istiyorsan kendisine ulas ve yardim et.")




if __name__ == "__main__":
    sender = MailSender(token=KEY, sender_mail=SENDER)
    sender.send_ticket(receiver="erkamesen789@gmail.com", link="deneme.com")



