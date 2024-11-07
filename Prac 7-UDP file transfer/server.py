from socket import *

def receive_file():
    host = "0.0.0.0"  # Listen on all interfaces
    port = 9999       # Port to listen on
    buf = 1024        # Buffer size

    # Set up the UDP socket
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((host, port))  # Bind the server to listen on all interfaces at the specified port
    print(f"Server listening on {host}:{port}...")

    # Open the file to save incoming data
    with open("received_file.txt", 'w') as f:
        print("Ready to receive file...")

        # Receive the file name first
        data, addr = s.recvfrom(buf)
        file_name = data.decode()
        print(f"Receiving file: {file_name}")

        # Receive the file data in chunks until <EOF> is received
        try:
            while True:
                data, addr = s.recvfrom(buf)
                
                # Check for the end-of-file signal
                if data.decode() == "<EOF>":
                    print("End of file signal received.")
                    break
                
                # Write the received data to the file
                f.write(data.decode())
                print(f"Received {len(data)} bytes...")

        except Exception as e:
            print(f"Error during file reception: {e}")

        finally:
            print("File download complete.")
            s.close()

if __name__ == "__main__":
    receive_file()
