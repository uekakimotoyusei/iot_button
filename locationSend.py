#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import json
import os
import boto3

TABLE_NAME = 'test_table'
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    url = 'https://api.line.me/v2/bot/message/push'
    channel_access_token = os.environ.get("CHANNEL_ACCESS_TOKEN")
    #useridをDBから取得する
    imsi = context.client_context.custom['imsi']
    
    res = dynamodb.get_item(TableName=TABLE_NAME, Key={
        'imsi': {'S': imsi}
    })
    userId = res['Item']['userid']['S']
    print(json.dumps(context.client_context.custom))
    lat = context.client_context.custom['location']['lat']
    lon = context.client_context.custom['location']['lon']
    # 送信用のデータ
    data = {
        'to' : userId,
        'messages' : [
            {
                'type' : 'location',
                'title': 'タイトル',
                'address': 'アドレス',
                'latitude': lat,
                'longitude': lon
            }
        ]
    }
    jsonstr = json.dumps(data)
    print(jsonstr)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + channel_access_token
    }
    request = urllib.request.Request(url, jsonstr.encode(), headers, method='POST')
    with urllib.request.urlopen(request) as res:
        ret = res.read()
    print('Response:', ret)
