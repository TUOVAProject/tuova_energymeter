import json
import time
from datetime import datetime
from pymodbus import client as modbus_client
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import schedule
from tuova_energymeter import modbus
from tuova_energymeter import influx

# disable "unverified https" warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    # get config params
    config = None
    with open("./config.json", "r") as f:
        config = json.loads(f.read())

    if config == None:
        print("main - no config")
        return -1
    
    # create modbus client
    mb_client = modbus_client.ModbusSerialClient(port=config["serial_path"], baudrate=config["serial_baud"])
    mb_client.connect()

    # create influx client
    in_client = influxdb_client.InfluxDBClient(url=config["influx_url"], org=config["influx_org"], token=config["influx_token"], verify_ssl=False)
    in_client_api = in_client.write_api(write_options=SYNCHRONOUS)
    config["in_client_api"] = in_client_api

    # thing to loop
    def measure():
        # get data
        data = modbus.read_data(opts={"mb_client":mb_client})
        # create timestamp
        ts = int(datetime.timestamp(datetime.now()) * 1000)
        # send data to influx
        influx.write_data(data=data, ts=ts, opts=config)

    print("main - start...")
    measure()

    # loop the thing
    schedule.every(1).seconds.do(measure)

    while True:
        schedule.run_pending()
        time.sleep(0.1)

if __name__ == "__main__":
    main()
