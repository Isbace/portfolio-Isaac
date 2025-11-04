import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, body, from_email, password, smtp_server, smtp_port):
    try:
        # Set up the email
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(from_email, password)

        # Send the email
        server.sendmail(from_email, to_email, message.as_string())
        print(f"Email sent to {to_email}")

        # Close the server connection
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example
name = "Emily Johnson"
car_plate = "ABC-1234"
fine_price = 150.75

# Construct the body
body = f"""
Hello {name},

This is a notification regarding a recent traffic violation. Below are the details:

- Car Plate: {car_plate}
- Fine Amount: ${fine_price:.2f}

Please ensure the payment is made at your earliest convenience to avoid additional penalties.

Thank you,
Campus Safety
"""

institution_email = "hernandezab@jbu.edu"
subject = "Traffic Violation Notice"
from_email = "BautistaI@jbu.edu" ## use su email
password = " " ## use your own password
smtp_server = "smtp.jbu.edu" 
smtp_port = 587 

send_email(institution_email, subject, body, from_email, password, smtp_server, smtp_port)