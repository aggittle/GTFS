import eventlet
eventlet.monkey_patch()
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict, MessageToJson
import requests
import time
import json
from celery import Celery
from flask_celery import make_celery
from celery.contrib.abortable import AbortableTask
import pandas as pd
from collections import OrderedDict, defaultdict
import numpy as np
from functools import reduce
from flask_socketio import SocketIO, emit
from flask import render_template, request, Flask, escape, Response
from time import sleep
from threading import Thread, Event

stop_ids = pd.read_csv('https://openmobilitydata-data.s3-us-west-1.amazonaws.com/public/feeds/mta/79/20181221/original/stops.txt')
urls = ['https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace',
'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm',
'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g',
'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz',
'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw',
'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l',
'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs',
'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-si'
]

def get_feed(url):
    try:
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(url, headers={"x-api-key":"m8cxK31C2e1rGSde1LvaN6zfCvwEHeGua9E9ivfP"})
        feed.ParseFromString(response.content)
        dict_obj = MessageToDict(feed)
        if dict_obj != {}:
            print(dict_obj)
            return dict_obj['entity']
        else:
            print('EMPTY FEED')
            return []
    except:
        print('PROBLEM GETTING FEED')

def get_time(stop, direction):
    print('GETTING TIME')
    #get feed
    for url in urls:
        if get_feed(url) is None:
            print('WARNING: ' + url + ' returned None')
    feeds = [get_feed(url) for url in urls if get_feed(url) is not None]
    dict_obj = reduce(lambda a,b: a+b, feeds)
    collector = []
    #turn stop into stop id

    stop_id = stop_ids.loc[(stop_ids['stop_name']==stop), 'stop_id'].tolist()


    # turn feed dict object into DataFrame
    for block in dict_obj:

        row = OrderedDict()
        try:
            row['id'] = block['id']
            row['tripId'] = block['tripUpdate']['trip'].get('tripId','')
            row['routeId'] = block['tripUpdate']['trip'].get('routeId','')
            for i, _stop in enumerate(block['tripUpdate']['stopTimeUpdate']):
                minutes = round((int(_stop['arrival'].get('time','')) - int(time.time()))/60)
                row[i] = (_stop['stopId'], minutes)

            collector.append(row)
        except:
            pass

        df = pd.DataFrame(collector)

    # print out timetables for given stop_id
    #print_list = []
    print_dict = defaultdict(list)
    for i, row in df.iterrows():
        for  j in row[3:]:
            if type(j) == tuple:
                if j[0] in stop_id and j[0].endswith(direction):
                    print_dict[str(row.routeId)].append(j[1])
    for key, value in print_dict.items():
        print_dict[key] = [str(int(x)) for x in sorted(value)]
                    #print_list.append((str(row.routeId) + ' arriving in ' + str(j[1]) + ' minutes', str(row.tripId)))
    return print_dict
