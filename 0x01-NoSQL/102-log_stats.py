#!/usr/bin/env python3
'''A script that prints statistics about NGINX logs.'''
from pymongo import MongoClient


def print_nginx_logs_stats(nginx_collection):
    '''A function that prints statistics about Nginx request logs.'''
    print('{} logs'.format(nginx_collection.count_documents({})))
    print('Methods:')
    meths = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for meth in meths:
        req_count = len(list(nginx_collection.find({'method': meth})))
        print('\tmethod {}: {}'.format(meth, req_count))
    status_checks_count = len(list(
        nginx_collection.find({'method': 'GET', 'path': '/status'})
    ))
    print('{} status check'.format(status_checks_count))


def print_top_http_ips(server_collection):
    '''Prints statistics about the top 10 HTTP IPs in a collection.
    '''
    print('IPs:')
    request_logs = server_collection.aggregate(
        [
            {
                '$group': {'_id': "$ip", 'totalRequests': {'$sum': 1}}
            },
            {
                '$sort': {'totalRequests': -1}
            },
            {
                '$limit': 10
            },
        ]
    )
    for request_log in request_logs:
        ip = request_log['_id']
        ip_requests_count = request_log['totalRequests']
        print('\t{}: {}'.format(ip, ip_requests_count))


def run_nginx():
    '''Provides some statistics about NGINX logs stored in MongoDB.
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_logs_stats(client.logs.nginx)
    print_top_http_ips(client.logs.nginx)


if __name__ == '__main__':
    run_nginx()
