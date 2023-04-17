from django.core.mail import send_mail
from django.template.loader import render_to_string
from artistx import settings
from django.core.mail import EmailMessage
from django.conf import settings

DOMAIN = settings.ALLOWED_HOSTS_URI

def send_email(to, profile_id, subject, url):
    message = render_to_string(
        'auth_app/email.html',
        context={
            "domain" : DOMAIN,
            "profile_id" : profile_id,
        }
    )
    email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            to
        )

    email.fail_silently = False
    email.send()
    # done = send_mail("Account Created Successfully on ArtistX", message, EMAIL_HOST, to, fail_silently=True)
    return True
    # except:
    #     return False

def update_profile(data, profile):
    profile.dob = data.get('dob') or profile.dob
    profile.country = data.get('country') or profile.country
    profile.state = data.get('state') or profile.state
    profile.currency_code = data.get('currency_code') or profile.currency_code
    profile.profile_headline = data.get('profile_headline') or profile.profile_headline
    profile.description = data.get('description') or profile.description
    return profile