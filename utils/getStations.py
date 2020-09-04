import requests
import json
import pymongo

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myClient['12306Spy']
mycol = mydb['station']

def getLastStations():
    r = requests.get('https://kyfw.12306.cn/otn/resources/js/framework/station_name.js')
    payload = r.content.decode('utf-8').replace('var station_names =\'@', '')[:-2]
    stations = payload.split('@')
    for index, station in enumerate(stations):
        station = station.split('|')
        stations[index] = {
            'id': station[5],
            'name': station[1],
            'teleCode': station[2],
            'pingyin': station[3],
            'firstPY': station[4],
            'pingyinCode': station[0]
        }
        mycol.insert_one(stations[index])
    return stations

def getStationInfo(stationName):
    station = mycol.find_one({'name': stationName})
    return station

# update stations info
# getLastStations()