#!/usr/bin/env python3
"""
python script that provides some stats about some
NGINX logs stored in mongo db
"""
from pymongo import MongoClient


client = MongoClient('mongodb://127.0.0.1:27017')
logs_collection = client.logs.nginx
count = logs_collection.count_documents({})
print("{} logs".format(count))
print("Methods:")
count_get = logs_collection.count_documents({"method": "GET"})
count_post = logs_collection.count_documents({"method": "POST"})
count_put = logs_collection.count_documents({"method": "PUT"})
count_patch = logs_collection.count_documents({"method": "PATCH"})
count_delete = logs_collection.count_documents({"method": "DELETE"})
print("\tmethod GET: {}".format(count_get))
print("\tmethod POST: {}".format(count_post))
print("\tmethod PUT: {}".format(count_put))
print("\tmethod PATCH: {}".format(count_patch))
print("\tmethod DELETE: {}".format(count_delete))
count_status = logs_collection\
        .count_documents({"method": "GET", "path": "/status"})
print("{} status check".format(count_status))
