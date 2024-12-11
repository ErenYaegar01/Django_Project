# utils.py
import random
from twilio.rest import Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

def generate_otp():
    """Generate a 6-digit OTP."""
    otp = random.randint(100000, 999999)  # Generate a random 6-digit number
    return otp

def send_otp(phone_number, otp):
    """Send OTP via SMS using Twilio."""
    # Twilio Configuration
    TWILIO_ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
    TWILIO_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
    TWILIO_PHONE_NUMBER = settings.TWILIO_PHONE_NUMBER

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is: {otp}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid # Return message SID for confirmation

def send_otp_email(email, otp):
    """Send OTP via email."""
    subject = "Your OTP for Login"
    message = f"Your one-time password is: {otp}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    
User = get_user_model()
def find_user_by_phone(phone_number):
    try:
        user = User.objects.get(phone_number=phone_number)
        return user
    except User.DoesNotExist:
        return None