from email.mime.text import MIMEText
import smtplib


def send_email(email, height, avg_height, num_of_users):
    from_email = "nirhersh15@gmail.com"
    from_password = "noanir1234"
    to_email = email

    subject = "Height data"
    message = "Hey there, your height is <strong>%s</strong>.\nThe average height of %s people that took the survey is" \
              " <strong>%s<strong>. " % (height, num_of_users, avg_height)

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)