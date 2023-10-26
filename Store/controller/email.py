from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings






def send_otyp_email(email, name, otp):
    
    html_content = render_to_string(
        'emailOTP.html', {'username': name, 'otp': otp})
    
    subject = 'Account verification OTP'
    send_mail(subject, '',settings.EMAIL_HOST_USER,
              [email], html_message=html_content)
    