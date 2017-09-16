#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import os
import logging

username = 'user@gmail.com'
password = 'secretpassword'


def retrive_all_receipts(username, password, directory='./receipts'):
    s = requests.Session()
    payload = {'username': username, 'password': password}
    header = {'Host': 'no.storebox.com',
              'Origin':  'https://no.storebox.com',
              'Connection': 'Keep-Alive',
              'Content-Type': 'application/json'}
    login_url = 'https://no.storebox.com/api/v1/authenticate'
    base_url = 'https://no.storebox.com/api/v1/receipts'
    login = s.post(login_url, headers=header, json=payload)
    if not login.status_code == 200:
        logger.info('login failed, HTTP STATUS: {}'.format(login.status_code))
        return

    r = s.get(base_url)
    receipts = json.loads(r.content.decode('utf-8'))
    check_storage_dir(directory)
    files = (os.listdir(directory))

    for x in receipts['receipts']:
        if x['receiptId'] in files:
            continue
        logger.info('Downloading: {}'.format(x['receiptId']))
        url = '{}/{}'.format(base_url, x['receiptId'])
        r = s.get(url)
        if r.status_code != 200:
            logger.info('requests failed: {} on {}'.format(r.status_code, url))
            continue
        path = '{}/{}'.format(directory, x['receiptId'])
        receipts = json.loads(r.content.decode('utf-8'))
        with open(path, 'w') as f:
            f.write(json.dumps(receipts))


def check_storage_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('storebox')
retrive_all_receipts(username, password)
