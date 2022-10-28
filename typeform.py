from config import *

import json
import requests


def get_signup_responses():
    endpoint = "https://api.typeform.com/forms/{}/responses".format(TYPEFORM_SIGNUP_FORM_ID)
    headers = {"Host": "api.typeform.com", "Accept": "application/json", "Accept-Language": "en-us",
               "Authorization": TYPEFORM_AUTH, "Cache-Control": "max-age=0", "Connection": "keep-alive"}
    try:
        response = requests.get(endpoint, headers=headers, timeout=30)
        if response.status_code == 200:
            phone_numbers = []
            json_response = json.loads(response.text)
            for item in json_response["items"]:
                for answer in item["answers"]:
                    if answer["type"] == "phone_number":
                        phone_numbers.append(answer["phone_number"])
                        break

            return phone_numbers, None

        else:
            return [], "Bad Status Code: " + str(response.status_code)

    except Exception as error:
        return [], str(error)


def get_scholarship_responses():
    endpoint = "https://api.typeform.com/forms/{}/responses".format(TYPEFORM_SCHOLARSHIP_FORM_ID)
    headers = {"Host": "api.typeform.com", "Accept": "application/json", "Accept-Language": "en-us",
               "Authorization": TYPEFORM_AUTH, "Cache-Control": "max-age=0", "Connection": "keep-alive"}
    try:
        response = requests.get(endpoint, headers=headers, timeout=30)
        if response.status_code == 200:
            scholarships = []
            json_response = json.loads(response.text)
            for item in json_response["items"]:
                sc_dict = {}
                for answer in item["answers"]:
                    if answer["field"]["id"] == TITLE_FIELD_ID:
                        sc_dict["title"] = answer["text"]

                    elif answer["field"]["id"] == URL_FIELD_ID:
                        sc_dict["url"] = answer["text"]

                    elif answer["field"]["id"] == ELIGIBILITY_FIELD_ID:
                        sc_dict["eligibility"] = answer["text"]

                    elif answer["field"]["id"] == AMOUNT_FIELD_ID:
                        sc_dict["amount"] = answer["text"]

                    elif answer["field"]["id"] == DEADLINE_FIELD_ID:
                        sc_dict["deadline"] = answer["text"]

                scholarships.append(sc_dict)

            return scholarships, None

        else:
            return [], "Bad Status Code: " + str(response.status_code)

    except Exception as error:
        return [], str(error)
