from random import choice, normalvariate, random
import requests
from api_config import RANDOM_PEOPLE_API_URL


def customer_data_generator(noise_count=30):
    customers = requests.request("GET", RANDOM_PEOPLE_API_URL).json()

    expected_cluster_values = {
        "18-25": {
            "amount_spent_online": 500,
            "amount_spent_in_store": 50,
            "hours_in_store": 10,
            "hours_online": 1,
        },

        "26-40": {
            "amount_spent_online": 1000,
            "amount_spent_in_store": 1000,
            "hours_in_store": 20,
            "hours_online": 20,
        },

        "41-60": {
            "amount_spent_online": 500,
            "amount_spent_in_store": 400,
            "hours_in_store": 10,
            "hours_online": 8,
        },

        "61+": {
            "amount_spent_online": 50,
            "amount_spent_in_store": 500,
            "hours_in_store": 1,
            "hours_online": 10,
        },
    }

    for customer in customers[:-noise_count]:
        age_group, expected_values = choice(list(expected_cluster_values.items()))
        customer["age_group"] = age_group

        for key, value in expected_values.items():
            customer[key] = round(max(0, value + normalvariate(0, 80)), 2)

        customer["products"] = [product for product in ["BELT", "T-SHIRT", "WALLET", "TV", "PHONE", "WATCH", "MUG"] if
                                random() < .3]

    for customer in customers[-noise_count:]:
        customer["age_group"] = choice(list(expected_cluster_values.keys()))
        customer["amount_spent_online"] = round(max(0., 1000 * random()), 2)
        customer["amount_spent_in_store"] = round(max(0., 1000 * random()), 2)
        customer["hours_online"] = round(max(0., normalvariate(1, .25) * customer["amount_spent_online"] / 20), 2)
        customer["hours_in_store"] = round(max(0., normalvariate(1, .25) * customer["amount_spent_in_store"]), 2)

        customer["products"] = [product for product in ["BELT", "T-SHIRT", "WALLET", "TV", "PHONE", "WATCH", "MUG"] if
                                random() < .3]

    return customers
