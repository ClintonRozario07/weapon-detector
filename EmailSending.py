import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import threading

send_event = threading.Event()

def send_mail():
    while True:
        send_event.wait()
        send_event.clear()

        age_file = open("age.txt","r+")

        # Setup an email server
        subject = "A weapon is detected!"
        body = "- Weapon is detected. \n- Maybe crime will happen by a person. \n- Whose probable detials are : \n" + age_file.read()
        sender_email = "mail.server.tech@gmail.com"
        receiver_email = "klintonrozario@gmail.com"
        password = "tuns rrbt xpio gjmx"

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        age_file.close()

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        filename = 'weapon.png'  # In same directory as script

        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, text)
            print("Email sent successfully")
        except Exception as e:
            print(f"Email could not be sent. Error: {str(e)}")
        
        #reset wait...
        send_event.wait()