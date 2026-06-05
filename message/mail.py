import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

def send_mail(name,subject,email,message,phone):
    my_email = os.getenv('my_email')
    email_password = os.getenv('email_password')
    try:
        html = f"""
        <html>
        <body>
        <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2 style="color:#2563eb;">Thank You for Contacting Me</h2>
    
    <p>Dear <b>{name}</b>,</p>
    
    <p>
        Thank you for reaching out through my portfolio website. I have successfully received your message and appreciate your interest.
    </p>
    
    <p>
        Below is a summary of the information you submitted:
    </p>
    
    <table style="border-collapse: collapse; width: 100%; max-width: 700px;">
        <tr>
            <td style="padding:8px;border:1px solid #ddd;"><b>Name</b></td>
            <td style="padding:8px;border:1px solid #ddd;">{name}</td>
        </tr>
        <tr>
            <td style="padding:8px;border:1px solid #ddd;"><b>Email</b></td>
            <td style="padding:8px;border:1px solid #ddd;">{email}</td>
        </tr>
        <tr>
            <td style="padding:8px;border:1px solid #ddd;"><b>Phone</b></td>
            <td style="padding:8px;border:1px solid #ddd;">{phone}</td>
        </tr>
        <tr>
            <td style="padding:8px;border:1px solid #ddd;"><b>Subject</b></td>
            <td style="padding:8px;border:1px solid #ddd;">{subject}</td>
        </tr>
        <tr>
            <td style="padding:8px;border:1px solid #ddd;"><b>Message</b></td>
            <td style="padding:8px;border:1px solid #ddd;">{message}</td>
        </tr>
    </table>
    
    <br>
    
    <p>
        I will review your inquiry and get back to you as soon as possible. If additional information is required, I will contact you using the email address you provided.
    </p>
    
    <p>
        Thank you for your time and interest. I look forward to connecting with you.
    </p>
    
    <br>
    
    <p>
        Best Regards,<br>
        <b>Prakash Singh</b><br>
        Software Engineer | Python Developer | MERN Stack Developer
    </p>
    
    <hr>
    
    <p style="font-size:12px;color:#666;">
        This is an automated confirmation email generated from my portfolio website. Please keep this email for your reference.
    </p>

</body>
</html>

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