"""


"""

from acq_common import acq_client

#add comments to files
def setup_server():
    client = acq_client.acq_Client()
    #change to local - check it works
    client.connect_to_server("tcp://localhost:50000")
    
    return client

def get_data(client):
    #determine number of frames to fetch from dt?
    data, md = client.fetch_data_product([-3, -2, -1, 0])
    print(data.shape)
    print(md)
    
    #from tutorial slides - array.reshape(-1, array[:,:,start_index:end_index].shape[2])
    output = data.reshape(-1, data.shape[2])
    print(output.shape)
    
    return output