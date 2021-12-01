import smtplib
from email.message import EmailMessage
from lib.actions import BaseAction


class SendMail(BaseAction):
    def run(self, username, password, recipient_address):

        mail_text = self.config.get('mail_text')
        mail_text_rendered = mail_text.format(username=username, password=password)

        msg = EmailMessage()
        msg['From'] = self.config.get('mail_sender_address')
        msg['To'] = recipient_address
        msg['Subject'] = self.config.get('mail_subject')
        msg.set_content(mail_text_rendered)

        try:
            server_instance = smtplib.SMTP(self.config.get('mail_server'))
            server_instance.send_message(msg)
        except Exception as e:
            self.logger.error(e)
            return False, ""
        finally:
            if server_instance:
                server_instance.quit()

        return True, "Mail transmitted successfully!"
