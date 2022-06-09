import json
from random import choice, normalvariate
import requests
from api_config import RANDOM_PEOPLE_API_URL

customers = requests.request("GET", RANDOM_PEOPLE_API_URL).json()

expected_cluster_values = {
    "18-25": {
        "amount_spent_online": 500,
        "amount_spent_in_store": 10,
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
        "amount_spent_online": 10,
        "amount_spent_in_store": 500,
        "hours_in_store": 1,
        "hours_online": 10,
    },
}

for customer in customers:
    age_group, expected_values = choice(list(expected_cluster_values.items()))
    customer["age_group"] = age_group

    for key, value in expected_values.items():
        customer[key] = round(max(0, value + normalvariate(0, 50)), 2)

with open("customers.json", "w") as f:
    json.dump(customers, f)
