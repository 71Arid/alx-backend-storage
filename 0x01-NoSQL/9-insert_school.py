#!/usr/bin/env python3
"""
inserting a document to a collection
based on kwargs returning new _id
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    using kwargs.tiems to access kwargs elements
    and getting id using inserted_id
    """
    document = {}
    for k, v in kwargs.items():
        document[k] = v
    obj = mongo_collection.insert_one(document)
    return obj.inserted_id
