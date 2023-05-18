import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# TODO: Убрать принты перед деплоем.
# На время разработки нам коды всё равно не нужны, поэтому лучше держать службу выключенной.
class MailSender:
    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password
        self.server = self.connect()
        print('[MailService] Connected!')

    def connect(self):
        server = smtplib.SMTP('smtp.zoho.com', 587)
        server.starttls()
        server.login(self.email, self.password)
        return server

    def send_code(self, code: str, target_email: str):
        print('[MailService]', target_email, code)
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = target_email
        msg['Subject'] = 'Код подтверждения - POTOM-PRIDUMAYU'
        msg.attach(MIMEText(f'Ваш код для подтверждения: {code}\n\nВведите его на сайте. Код действителен 10 минут',
                            'plain'))
        self.server.send_message(msg)
        print('[MailService] Successful')
