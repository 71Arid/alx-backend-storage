#!/usr/bin/env python3
"""
changes all topics of a school based on the name
topics is a list of strings
"""
import pymongo


def update_topics(mongo_collection, name, topics):
    """
    uses update_one to update the parameter
    "dict parameter"
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
