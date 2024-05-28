
def toggle():
    text_file = read_bin_file()
    print(text_file)
    data = "on" if (text_file == "off") else "off"
    print(data)
    save_bin_file(data)


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
