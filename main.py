import json
from datetime import datetime
from pymodbus import client
from tuova_energymeter import modbus
from tuova_energymeter import influx

def main():
    # get config params
    config = None
    with open("./config.json", "r") as f:
        config = json.loads(f.read())

    if config == None:
        print("main - no config")
        return -1
    
    # create modbus client
    mb_client = client.ModbusSerialClient(port=config["serial_path"], baudrate=config["serial_baud"])
    mb_client.connect()

    # create influx client

    # TODO: LOOP

    # get data
    data = modbus.read_data(opts={"mb_client":mb_client})

    # create timestamp
    ts = int(datetime.timestamp(datetime.now()) * 1000)
    
    # send data to influx
    influx.write_data(data=data, ts=ts, opts=config)


if __name__ == "__main__":
    main()
