from smtplib import SMTP


KEY = "psmieqvitnjplcmj"
SENDER = "batkar.fest@gmail.com"

class MailSender:
    
    def __init__(self, token, sender_mail, 
                 mail_server="smtp.gmail.com", port=587):
        
        self.token = token
        self.sender_mail = sender_mail
        self.mail_server = mail_server
        self.port = port

    def send_password_link(self, receiver, link):
        with SMTP(self.mail_server, self.port) as connection:  
            connection.starttls()  
            connection.login(self.sender_mail, password=self.token)  
            connection.sendmail(from_addr=self.sender_mail,
                                            to_addrs=receiver,
                                            msg=f"Subject:Reset Password!\n\nYou can reset your password by following the link below:\n\n{link}")


sender = MailSender(token=KEY, sender_mail=SENDER)

sender.send_password_link(receiver="erkamesen789@gmail.com", link="deneme.com")



