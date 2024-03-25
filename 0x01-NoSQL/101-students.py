#!/usr/bin/env python3
'''A script that returns all the average scores of the students'''


def top_students(mongo_collection):
    '''A function that Prints all students in a collection sorted by averag'''
    my_students = mongo_collection.aggregate(
        [
            {
                '$project': {
                    '_id': 1,
                    'name': 1,
                    'averageScore': {
                        '$avg': {
                            '$avg': '$topics.score',
                        },
                    },
                    'topics': 1,
                },
            },
            {
                '$sort': {'averageScore': -1},
            },
        ]
    )
    return my_students
