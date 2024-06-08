import re

import smartSwitchLib.ACME as ACME
import smartSwitchLib.discover as smartSwitchLib
import json


def toggle():
    res = ACME.get_data_from_container('SmartSwitch', 'SmartSwitch', smartSwitchLib.get_hash_mac_address())
    print(f"----------------------\n{res}\n-------------------")
    pairs = str(res).split(',')

    # Initialize message variable
    message = None

    pattern = r"'con':\s*'({.*?})'"

    # Search for the pattern in the data
    match = re.search(pattern, str(res))

    # If a match is found
    if match:
        # Extract the value associated with the key 'con'
        message_json = match.group(1)
        # Parse the JSON string to extract the message
        message = re.search(r'"message"\s*:\s*"([^"]+)"', message_json).group(1)
        print("Message:", message)
    else:
        print("No status was found.")

    data = "ON" if (message == "OFF") else "OFF"
    return data


def save_bin_file(data):
    binary_data = data.encode('utf-8')
    with open('status.bin', 'wb') as file:
        # Write the binary data to the file
        file.write(binary_data)


def read_bin_file():
    try:
        # Try to open the file for reading in binary mode
        with open('status.bin', 'rb') as file:
            print("File opened successfully.")
            # Read the binary data from the file
            binary_data = file.read()
    except FileNotFoundError:
        # If the file doesn't exist, create it with some initial binary data
        with open('status.bin', 'wb') as file:
            data = b'off'  # Initial binary data
            file.write(data)
            print("File created successfully with initial binary data.")
        # Return the initial data
        return data

    # Convert binary data to text using UTF-8 encoding
    text_data = binary_data.decode('utf-8')
    # Print the text data
    return text_data
