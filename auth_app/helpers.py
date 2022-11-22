from django.core.mail import send_mail
from django.template.loader import render_to_string
from artistx import settings
from .models import Profile
from .serializers import ProfileSerializer

DOMAIN = settings.ALLOWED_HOSTS_URI
EMAIL_HOST = "gourav.19b131001@abes.ac.in"

def send_email(to, profile_id):
    message = render_to_string(
        'auth_app/email.html',
        context={
            "domain" : DOMAIN,
            "profile_id" : profile_id
        }
    )
    print(message)
    done = send_mail("Account Created Successfully on ArtistX", message, EMAIL_HOST, to, fail_silently=True)
    print(done)
    return

def update_profile(data, profile:Profile):
    profile.dob = data.get('dob') or profile.dob
    profile.country = data.get('country') or profile.country
    profile.state = data.get('state') or profile.state
    profile.currency_code = data.get('currency_code') or profile.currency_code
    profile.profile_headline = data.get('profile_headline') or profile.profile_headline
    profile.description = data.get('description') or profile.description
    return profile