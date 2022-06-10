from django.core.mail import send_mail

from django.conf import settings

def send_email_pass_forgot(email,token):
    subject = " your forget password link "
    message = f" click the link for change password http://127.0.0.1:8000/change_pass/{token}/"
    email_from = settings.EMAIL_HOST_USER
    recepient_list = [email]
    send_mail(subject,message,email_from,recepient_list)
    return True

def send_email_to_active_user(email,token):
    subject = " to active your account click thi link "
    message = f" click the link for change password http://127.0.0.1:8000/active_user/{token}/"
    email_from = settings.EMAIL_HOST_USER
    recepient_list = [email]
    send_mail(subject,message,email_from,recepient_list)
    return True    
