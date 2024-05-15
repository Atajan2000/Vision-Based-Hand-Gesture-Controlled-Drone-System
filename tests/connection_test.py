from dronekit import connect

if __name__ == '__main__':

    connection_string = "tcp:192.168.10.7:6000"

    print('1. Connection test:')
    try:
        vehicle = connect(connection_string, wait_ready=True, timeout=60)
        print("Connected successfully to: " + connection_string)
    except Exception as e:
        print("Error connecting to vehicle: ", str(e))
    print('\n')

    vehicle.close()
    print("Connection closed.")
