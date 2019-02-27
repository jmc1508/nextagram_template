import sendgrid
from instagram_web import sg
from sendgrid.helpers.mail import *

# Connect to SENDGRID using API Key


def send_donation_email(receiver, amount, sender):
    from_email = Email(sender)
    to_email = Email(receiver)
    subject = "Sending with SendGrid is Fun"
    content = Content(
        "text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    return response
