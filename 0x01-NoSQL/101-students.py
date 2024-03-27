#!/usr/bin/env python3
"""
function that returns all students sorted by average
score
"""
import pymongo


def top_students(mongo_collection):
    """
    unwinded the array so as to enable each doc to have
    one score
    grouped by id
    """
    res = mongo_collection.aggregate([
        {
            "$unwind": "$topics"
        },
        {
            "$group": {
                "_id": "$_id",
                "name": {"$first": "$name"},
                "averageScore": {
                    "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ])
    return res
