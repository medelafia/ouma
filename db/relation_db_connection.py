from influxdb import InfluxDBClient




def get_influx_connection() : 

    try : 
        client = InfluxDBClient(host='localhost', port=8086)


        return client
    except Exception as ex:
        print("exception occured " , ex )