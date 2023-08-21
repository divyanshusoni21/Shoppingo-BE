from django.core.mail import EmailMultiAlternatives
import threading
from .email_templates import  EmailTemplates
from .base_email import footer
from restra_backend.settings import logger

def get_body(data):
    emailType = data['type']
    content = EmailTemplates(data)
    
    if emailType == 'registration' :
        content = content.register()
    elif emailType == 'plan_expire' :
        content = content.plan_expired()
    
    content = footer(content)
    return content

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()
       
class Email:
    @staticmethod
    def send_email(data):
        try :
            html_body = ''
            html_body =  get_body(data['email_body'])
            email = EmailMultiAlternatives(
                        subject=data['email_subject'],
                        body='',
                        to=[data['to_email']]
                    )
            
            
            if html_body :
                email.attach_alternative(html_body,"text/html")
                EmailThread(email).start()
                logger.info(f'email send to {data["to_email"]} , subject :{data["email_subject"]}')
              
        except Exception as e :
            logger.warning(f'error in email send : {e}')