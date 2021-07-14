"""
es_client
​
Copyright (c) 2018 __CGD Inc__. All rights reserved.
"""
import os
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
from elasticsearch import Elasticsearch
from elasticsearch import RequestsHttpConnection
import yaml


with open('./config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

AppConfig = config['AppConfig']

__all__ = ['indices']

client_by_process = {}


def get_client():
    current_pid = os.getpid()

    if client_by_process.get(current_pid) is None:
        client_by_process[current_pid] = _get_client()
    return client_by_process[current_pid]





'''
Get ES client with auth
'''
def _get_client():
    if 'amazonaws' in AppConfig['ELASTICSEARCH_HOST']:
        awsauth = BotoAWSRequestsAuth(
            aws_host=AppConfig['ELASTICSEARCH_HOST_CANONICAL'],
            aws_region=AppConfig['ELASTICSEARCH_REGION'],
            aws_service='es'
        )
      
        return Elasticsearch(
            hosts=[AppConfig['ELASTICSEARCH_HOST']],
            http_auth=awsauth,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )
    else:
        client = Elasticsearch(
            hosts=[AppConfig['ELASTICSEARCH_HOST']]
        )
        return client


