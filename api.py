import scholarship_main
import signup_main
import sms
from config import *

import json
import threading
from flask import Flask
from flask import request

app = Flask(__name__)
users_file = "users.json"
scholarships_file = "scholarships.json"


@app.route("/")
def index():
    return "ScholarshipNotifier API v{}".format(API_VERSION)


@app.route("/api/enroll", methods=["POST"])
def enroll_user():
    with open(users_file, "r") as file:
        users_json = json.load(file)
        users = users_json["users"]

    phone_number = request.form["number"]
    formatted_number, verified = sms.verify_phone_number(phone_number)
    if verified:
        if formatted_number in users:
            return {"success": False, "error": "Duplicate phone number provided."}, 400

        else:
            users.append(formatted_number)
            with open(users_file, "w") as file:
                users_dict = {"users": users}
                file.write(json.dumps(users_dict))

            sms.send_welcome(formatted_number)
            return {"success": True, "error": None}

    else:
        return {"success": False, "error": "The provided phone number is not valid."}, 400


@app.route("/api/scholarships/add", methods=["POST"])
def add_scholarship():
    with open(scholarships_file, "r") as file:
        scholarships_json = json.load(file)
        scholarships = scholarships_json["scholarships"]

    authorization = request.headers.get("Authorization")
    if authorization == "Basic NTY5MmVhOWItNzBkYy00M2YxLTllMzEtOGE0ZGI5M2ZiZWUy":
        title = request.form["title"]
        url = request.form["url"]
        eligibility = request.form["eligibility"]
        amount = request.form["amount"]
        deadline = request.form["deadline"]

        duplicate = False
        for sc in scholarships:
            if title == sc["title"]:
                duplicate = True
                break

        if duplicate:
            return {"success": False, "error": "Duplicate scholarship provided."}, 400

        else:
            sc_dict = {"title": title, "url": url, "eligibility": eligibility, "amount": amount, "deadline": deadline}
            scholarships.append(sc_dict)

            with open(scholarships_file, "w") as file:
                scholarships_dict = {"scholarships": scholarships}
                file.write(json.dumps(scholarships_dict))

            return {"success": True, "error": None}

    else:
        return {"success": False, "error": "Unauthorized"}, 401


if __name__ == "__main__":
    signup_thread = threading.Thread(target=signup_main.main())
    scholarship_thread = threading.Thread(target=scholarship_main.main())
    signup_thread.start()
    scholarship_thread.start()
    app.run(host="0.0.0.0", port=3333)
