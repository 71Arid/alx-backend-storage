#!/usr/bin/env python3
"""
returns the list of schools having a specific
topic. Topic is string to be searched
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    use $in operator to find the topic
    passed in the available documents
    """
    topic = mongo_collection.find({"topics": {"$in": [topic]}})
    return [doc for doc in topic]
