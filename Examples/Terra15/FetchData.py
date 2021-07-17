from acq_common import acq_client
import sys
def main():
    client = acq_client.acq_Client()
    #server_ip = "127.0.0.1"
    #server_port = 48000
    #full_server_address = f"tcp://{server_ip}:{server_port}"
    client.connect_to_server("tcp://localhost:50000")
    #list client functions is: client.list_client_functions()
    data,md = client.fetch_data_product([-3,-2,-1,0]);
    print(data, file = sys.stdout)

if __name__ == '__main__':
    main()
