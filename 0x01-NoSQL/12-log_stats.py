#!/usr/bin/env python3
'''Nginx logs statistics.
'''
from pymongo import MongoClient


def print_nginx_request_stats(nginx_collection):
    '''A function that Prints stats about Nginx request logs.
    '''
    print('{} logs'.format(nginx_collection.count_documents({})))
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        req_count = len(list(nginx_collection.find({'method': method})))
        print('\tmethod {}: {}'.format(method, req_count))
    status_checks_count = len(list(
        nginx_collection.find({'method': 'GET', 'path': '/status'})
    ))
    print('{} status check'.format(status_checks_count))


def run_nginx():
    '''A function that provides some stats about Nginx logs stored in MongoDB.
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_stats(client.logs.nginx)


if __name__ == '__main__':
    run_nginx()