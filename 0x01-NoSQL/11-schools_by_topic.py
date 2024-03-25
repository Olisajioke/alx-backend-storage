#!/usr/bin/env python3
# Returns the list of schools having a specific topic.

def schools_by_topic(mongo_collection, topic):
    """Returns the list of schools having a specific topic."""
    filter_top = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [document for document in mongo_collection.find(filter_top)]