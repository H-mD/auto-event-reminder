import smtplib, ssl
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
import os

class Mailer: 
    def __init__(self, main_email, password, sender_email, smtp_server='smtp.gmail.com', port=587):
        self.main_email = main_email
        self.password = password
        self.sender_email = sender_email
        self.smtp_server = smtp_server
        self.port = port
        self.subject = "subject here"
    
    def set_body(self, event_name, event_date, event_time, event_location):
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('template_example.html')

        data = {
            'event_name': event_name,
            'event_date': event_date,
            'event_time': event_time,
            'event_location': event_location,
        }

        body = template.render(data)

        return MIMEText(body, 'html')
   
    def send_email(self, recipients, event_name, event_date, event_time, event_location):
        message = self.set_body(event_name, event_date, event_time, event_location)
        message["From"] = self.sender_email
        message["To"] = ", ".join(recipients)
        message["Subject"] = self.subject

        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls(context=ssl.create_default_context())
            try:
                server.login(self.main_email, self.password)
            except smtplib.SMTPAuthenticationError:
                return("[FAILED] Failed to log in to the SMTP server. Please check your email address and password.")
            
            try:
                server.sendmail(self.sender_email, recipients, message.as_string())
                return f"[SUCCESS] Email successfully sent to {', '.join(recipients)}"
            except smtplib.SMTPRecipientsRefused:
                return ("[FAILED] Email Refused by the SMTP server. Please check the recipient's email address.")
            
if __name__ == '__main__':
    load_dotenv()
    m = Mailer(os.getenv('MAIN_EMAIL'), os.getenv('PASSWORD'), os.getenv('SENDER_EMAIL'), os.getenv('SMTP_SERVER'), os.getenv('SMTP_PORT'))
    context = ssl.create_default_context()
    recipients = ['example@mail.com', 'example2@gmail.com']
    print(m.send_email(recipients, "Event Name", "dd-mm-yyyy", "hh:mm", "Event Location"))