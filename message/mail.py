import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

def send_mail(name,subject,email):
    my_email = os.getenv('my_email')
    email_password = os.getenv('email_password')
    try:
        html = f"""
        <html>
        <body>
        <p>Dear <b>{name}</b>,</p>
        <p>our team contact you shortly</p>
        
        <p><b>Thank you for contacting us.</b></P>
        <p>if you received this mail please ignore <br> this is the testing mail for auto call log's</p>
        
        </body>
        </html>
        """



        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = my_email
        
        msg['To'] = email
        

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        #login
        server.login(my_email,email_password)
        
        msg.set_content("html attached below")
        msg.add_alternative(html,subtype='html')

        response = server.send_message(msg)


        server.quit()
        return {'status':"successful"}
    except Exception as e:
        return {
        "status": "failed",
        "error": str(e)
    }