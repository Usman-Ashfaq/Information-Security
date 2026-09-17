import socket
import struct
import cv2
import numpy as np

SERVER_IP = "0.0.0.0"      # listen on all interfaces
PORT = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_IP, PORT))
server_socket.listen(1)

print(f"Waiting for client on port {PORT}...")
client_socket, client_address = server_socket.accept()
print("Client connected:", client_address)

def recv_exact(sock, n):
    """Receive exactly n bytes, or return None if connection closed."""
    buf = b""
    while len(buf) < n:
        packet = sock.recv(n - len(buf))
        if not packet:
            return None
        buf += packet
    return buf

running = True
try:
    while running:
        # 1. Read 8-byte length header
        header = recv_exact(client_socket, 8)
        if header is None:
            print("Client disconnected.")
            break

        (length,) = struct.unpack(">Q", header)

        # 2. Read the JPEG payload
        frame_data = recv_exact(client_socket, length)
        if frame_data is None:
            print("Client disconnected mid-frame.")
            break

        # 3. Decode & show
        frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8),
                             cv2.IMREAD_COLOR)
        if frame is not None:
            cv2.imshow("Server - Client Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            running = False
finally:
    client_socket.close()
    server_socket.close()
    cv2.destroyAllWindows()
    print("Server stopped.")