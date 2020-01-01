from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict, MessageToJson
import urllib3
import requests
import time
import json
import pandas as pd
import datetime
from collections import OrderedDict
import numpy as np

stop_ids = pd.read_csv('stop_ids.csv')

def get_update():
    http = urllib3.PoolManager()
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get('http://datamine.mta.info/mta_esi.php?key=636e323a9180834b0811457aa7db81ce')
    feed.ParseFromString(response.content)
    dict_obj = MessageToDict(feed)
    collector = []

    for block in dict_obj['entity']:

        row = OrderedDict()
        try:
            row['id'] = block['id']

            row['trip_id'] = block['vehicle']['trip'].get('tripId','')
            row['route_id'] = block['vehicle']['trip'].get('routeId','')
            row['direction_id'] = block['vehicle']['trip'].get('directionId','')
            row['schedule_relationship'] = block['vehicle'].get('currentStatus','')


            row['start_date'] = block['vehicle']['trip'].get('startDate','')
            #row['latitude'] = block['vehicle']['position'].get('latitude','')
            #row['longitude'] = block['vehicle']['position'].get('longitude','')
            #row['bearing'] = block['vehicle']['position'].get('bearing','')
            row['current_stop_sequence'] = block['vehicle'].get('currentStopSequence','')
            row['current_status'] = block['vehicle'].get('currentStatus','')
            row['timestamp'] = block['vehicle'].get('timestamp','')
            row['stop_id'] = block['vehicle'].get('stopId','')
            #row['vehicle_id'] = block['vehicle']['vehicle'].get('id','')
            #row['label'] = block['vehicle']['vehicle'].get('label','')
            collector.append(row)
        except:
            pass

    df = pd.DataFrame(collector)

    feedtime = int(dict_obj['header']['timestamp'])
    print('Feed timestamp:',feedtime,',', datetime.datetime.fromtimestamp(feedtime))
    df['feed time'] = datetime.datetime.fromtimestamp(feedtime)

    df = pd.merge(df, stop_ids[['stop_id', 'stop_name']],  on='stop_id')

    print(df[((df.stop_id == '233N') |
   (df.stop_id == '234N') |
   (df.stop_id == '235N')  |
   (df.stop_id == '236N') |
   (df.stop_id == '237N') |
   (df.stop_id == '233S') |
   (df.stop_id == '234S') |
   (df.stop_id == '235S') |
   (df.stop_id == '236S'))][['current_status','route_id','stop_name', 'stop_id']])

while True:
    try:
        get_update()
        time.sleep(10)
    except:
        continue
