#!/usr/bin/python
import sys
import Adafruit_DHT
import datetime
from influxdb import InfluxDBClient

DB_HOST = "synology.lan"
DB_PORT = "8086"
DB_USER = ""
DB_PASSWORD = ""
DB_NAME = "weather"

v_humidity, v_temperature = Adafruit_DHT.read_retry(11, 4)
rv_temperature = '{0:0.1f}'.format(v_temperature,v_humidity)
rv_humidity = '{1:0.1f}'.format(v_temperature,v_humidity)

body_temperature = [
    {
        "measurement": "temperature",
        "tags": {
            "location": "outside",
        },
        "time": datetime.datetime.now(),
        "fields": {
            "value": rv_temperature
        }
    }
]

body_humidity = [
    {
        "measurement": "humidity",
        "tags": {
            "location": "outside",
        },
        "time": datetime.datetime.now(),
        "fields": {
            "value": rv_humidity
        }
    }
]

temp_client = InfluxDBClient(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, 'temp')
hum_client = InfluxDBClient(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, 'hum')

temp_client.switch_database(DB_NAME)
hum_client.switch_database(DB_NAME)

temp_client.write_points(body_temperature)
hum_client.write_points(body_humidity)
