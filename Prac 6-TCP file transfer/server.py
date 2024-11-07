import socket
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")

        """ Receiving the filename. """
        filename = conn.recv(SIZE).decode(FORMAT)
        print(f"[RECEIVED FILENAME]: {filename}")
        conn.send("Filename received.".encode(FORMAT))

        """ Preparing to receive the file data in chunks. """
        file_data = []
        while True:
            data = conn.recv(SIZE)
            if not data:
                break
            file_data.append(data.decode(FORMAT))

        file_data = ''.join(file_data)  # Combine all parts into one string

        """ Ensure 'data' directory exists and save the file. """
        if not os.path.exists("data"):
            print("[DEBUG] Creating 'data' directory.")
            os.makedirs("data")
        
        try:
            with open(f"data/received_{filename}", "w") as file:
                file.write(file_data)
            print(f"[SAVED] File saved as 'data/received_{filename}'")
            conn.send("File data received and saved.".encode(FORMAT))
        except Exception as e:
            print(f"[ERROR] Could not write to file: {e}")
            conn.send("Failed to save the file.".encode(FORMAT))

        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")

if __name__ == "__main__":
    main()
