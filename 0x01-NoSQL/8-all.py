#!/usr/bin/env python3
"""
python function that lists all documents
in a collection. Returns an empty list
if no dumnet is found in collection
"""
import pymongo


def list_all(mongo_collection):
    if mongo_collection is not None:
        return list()
    return list(mongo_collection)
