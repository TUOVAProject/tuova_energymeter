import json
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
    mb_client = ""
    modbus.read_data(opts={"mb_client":True})

    # TODO: loop

    # read and parse data
    # add timestamps
    
    # send data to influx
    influx.write_data()


if __name__ == "__main__":
    main()
