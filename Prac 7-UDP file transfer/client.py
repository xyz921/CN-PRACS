from socket import *

def send_file():
    host = "127.0.0.1"  # The server's IP address
    port = 9999         # The port on which the server is listening
    buf = 1024          # Buffer size
    filename = "test_file.txt"

    # Set up the UDP socket
    s = socket(AF_INET, SOCK_DGRAM)

    try:
        # Send the filename first
        s.sendto(filename.encode(), (host, port))
        print(f"Sent filename: {filename}")

        # Open the file and send its content in chunks
        with open(filename, 'r') as f:
            while True:
                data = f.read(buf)
                if not data:
                    break  # End of file reached
                s.sendto(data.encode(), (host, port))
                print(f"Sent {len(data)} bytes...")

        # Send an EOF marker to signal the end of the file transfer
        s.sendto("<EOF>".encode(), (host, port))
        print("Sent end-of-file signal.")

    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        s.close()

if __name__ == "__main__":
    send_file()
