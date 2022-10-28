from config import *

from twilio.base.exceptions import *
from twilio.rest import Client

# Creates Twilio client. Twilio is a communications API used for sending SMS
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# Sends a welcoming message to the user after they have signed up for the service
def send_welcome(recipient):
    message_body = "Thank you for signing up to receive text messages about available scholarships sent by your " \
                   "school!\n\nYou can opt-out of these messages at any time by replying with STOP "
    message = client.messages.create(
        body=message_body,
        messaging_service_sid=TWILIO_MESSAGE_SERVICE_SID,
        to=recipient
    )

    return message


# Sends a message via Twilio to a specified phone number
# Takes a Scholarship object as an input. This can be found in scholarships.py
def send_scholarship(scholarship, recipient):
    message_body = "A new scholarship is available!\n\n{}\n\nAmount: {}\nDeadline: {}\n\nEligibility: {}\n{}".format(
        scholarship.title, scholarship.amount, scholarship.deadline, scholarship.eligibility, scholarship.url)

    message = client.messages.create(
        body=message_body,
        messaging_service_sid=TWILIO_MESSAGE_SERVICE_SID,
        to=recipient
    )

    return message


# Verifies if a phone number is in a valid format via Twilio
def verify_phone_number(number):
    try:
        phone_number = client.lookups.v1.phone_numbers(number).fetch(country_code="US")
        return phone_number.phone_number, True

    except TwilioRestException:
        return "", False
