from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict, MessageToJson
import urllib3
import requests
import time
import json
import pandas as pd
import datetime
from collections import OrderedDict, defaultdict
import numpy as np
from functools import reduce

stop_ids = pd.read_csv('https://openmobilitydata-data.s3-us-west-1.amazonaws.com/public/feeds/mta/79/20181221/original/stops.txt')
urls = ['http://datamine.mta.info/mta_esi.php?key=636e323a9180834b0811457aa7db81ce',
'http://datamine.mta.info/mta_esi.php?key=636e323a9180834b0811457aa7db81ce&feed_id=16',
'http://datamine.mta.info/mta_esi.php?key=636e323a9180834b0811457aa7db81ce&feed_id=26',
'http://datamine.mta.info/mta_esi.php?key=636e323a9180834b0811457aa7db81ce&feed_id=21',
'http://datamine.mta.info/mta_esi.php?key=636e323a9180834b0811457aa7db81ce&feed_id=2',
'http://datamine.mta.info/mta_esi.php?key=636e323a9180834b0811457aa7db81ce&feed_id=31',
'http://datamine.mta.info/mta_esi.php?key=636e323a9180834b0811457aa7db81ce&feed_id=36',
'http://datamine.mta.info/mta_esi.php?key=636e323a9180834b0811457aa7db81ce&feed_id=51'
]

def get_feed(url):
    http = urllib3.PoolManager()
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(url)
    feed.ParseFromString(response.content)
    dict_obj = MessageToDict(feed)
    if dict_obj != {}:
        return dict_obj['entity']
    else:
        return []

def get_time(stop, direction):
    while True:
        #get feed
        feeds = [get_feed(url) for url in urls]
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
                for i, stop in enumerate(block['tripUpdate']['stopTimeUpdate']):
                    minutes = round((int(stop['arrival'].get('time','')) - int(time.time()))/60)
                    row[i] = (stop['stopId'], minutes)

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
                        print_dict[str(row.routeId)].append(str(j[1]) + ' minutes')
                        #print_list.append((str(row.routeId) + ' arriving in ' + str(j[1]) + ' minutes', str(row.tripId)))
        return print_dict
