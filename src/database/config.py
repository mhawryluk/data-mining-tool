import os

# fixes database connection on my wifi, to delete if it interferes with other networks
import dns.resolver
from pymongo import MongoClient

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ["8.8.8.8"]

client = MongoClient(
    "mongodb+srv://admin:{}@dataminingtooldb.trcgm.mongodb.net/".format(
        os.environ.get("MONGO_PASS")
    )
)
