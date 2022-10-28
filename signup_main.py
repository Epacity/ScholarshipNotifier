import sms
from config import *
from typeform import get_signup_responses

import json
import time


def get_users():
    with open(USERS_FILE, "r") as users_file:
        users_json = json.load(users_file)
        users = users_json["users"]

    return users


def main():
    users = get_users()
    print("Monitoring for new user signups...")
    while True:
        phone_numbers, error = get_signup_responses()
        if error:
            print("An error occured while fetching Typeform responses. Error: {}".format(error))

        else:
            for number in phone_numbers:
                if number not in users:
                    formatted_number, verified = sms.verify_phone_number(number)
                    if verified:
                        print("New signup detected! Number: {}".format(formatted_number))
                        users.append(formatted_number)
                        with open(USERS_FILE, "w") as file:
                            users_dict = {"users": users}
                            file.write(json.dumps(users_dict))

                        message = sms.send_welcome(formatted_number)

                        print("Welcomed user {}! (message ID: {})".format(formatted_number, message.sid))

        time.sleep(5)
