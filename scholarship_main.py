import sms
from config import *
from scholarships import Scholarship
from typeform import get_scholarship_responses

import json
import time


def get_users():
    with open(USERS_FILE, "r") as users_file:
        users_json = json.load(users_file)
        users = users_json["users"]

    return users


def get_scholarships():
    with open(SCHOLARSHIPS_FILE, "r") as scholarships_file:
        scholarships_json = json.load(scholarships_file)
        scholarships = scholarships_json["scholarships"]

    return scholarships


def main():
    scholarships = get_scholarships()
    print("Monitoring for new scholarships...")
    while True:
        new_scholarships, error = get_scholarship_responses()
        if error:
            print("An error occurred while fetching Typeform responses. Error: {}".format(error))

        else:
            for scholarship in new_scholarships:
                if scholarship not in scholarships:
                    print("New scholarship detected! Title: {}".format(scholarship["title"]))

                    scholarship_obj = Scholarship(scholarship["title"], scholarship["url"], scholarship["eligibility"],
                                                  scholarship["amount"], scholarship["deadline"])
                    users = get_users()
                    for user in users:
                        message = sms.send_scholarship(scholarship_obj, user)
                        print("Notified user {}! (message ID: {})".format(user, message.sid))

                    scholarships.append(scholarship)
                    with open(SCHOLARSHIPS_FILE, "w") as file:
                        scholarships_dict = {"scholarships": scholarships}
                        file.write(json.dumps(scholarships_dict))

        time.sleep(5)
