from acq_common import acq_client
from acq_common import json_utils # Helper functions to when working with json files
# Create an instance of an acquisition client
client = acq_client.acq_Client()
# Define the server ip address and connection port and build a full address based on˓→it.
server_ip = "127.0.0.1" # If running locally
server_port = 48000 # Default port
full_server_address = f"tcp://{server_ip}:{server_port}"
# Define the settings file to use when configuring the server
settings_file_path = "/home/terra15/treble_startup/default_treble_settings.json"
setup_string = json_utils.read_dict_from_json_file(settings_file_path)
# Connect the client instance to the server
client.connect_to_server(full_server_address)
# Configure the acquisition server
client.setup(setup_string)
# Start acquiring data
client.start_acquire()