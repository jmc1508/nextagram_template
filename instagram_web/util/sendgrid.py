import sendgrid
from instagram_web import sg
from sendgrid.helpers.mail import *
from pathlib import Path
import base64

# Connect to SENDGRID using API Key


def send_donation_email(receiver_email,receiver_username, sender_email,amount ):
    from_email = Email(sender_email)
    to_email = Email(receiver_email)
    subject = "Sending with SendGrid is Fun"
    content = Content(
        "text/html", 
        f"<h1>Hello</h1><p>You have donated {amount}</p>")

  

    # Declare Mail
    mail = Mail(from_email, subject, to_email, content)

    response = sg.client.mail.send.post(request_body=mail.get())

    return response

