import influxdb_client

def write_data(data:dict=None, ts=None, opts=None):

    if data == None or ts == None or opts == None:
        print("influx - write_data: err")
        return -1

    print("influx - write_data")

    client_api : influxdb_client.WriteApi = opts["in_client_api"]

    # create datapoint
    point = influxdb_client.Point(measurement_name=opts["influx_measurement"]).tag(key="sensor_id", value=opts["influx_sensor_id"]).time(time=ts, write_precision="ms")

    # append fields
    for f in data.keys():
        point.field(field=f, value=data[f])

    # send it
    try:
        client_api.write(bucket=opts["influx_bucket"], record=point)
    except Exception as ex:
        print("influx - write_data err:" + str(ex))
