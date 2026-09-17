import socket
import struct
import cv2

SERVER_IP = "10.54.4.222"   # <-- put the SERVER machine's real IP here
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))
print("Connected to server.")

camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Could not open camera.")
    client_socket.close()
    raise SystemExit

print("Camera started. Press Q to stop.")

try:
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Could not read frame.")
            break

        success, encoded = cv2.imencode(".jpg", frame,
                                        [cv2.IMWRITE_JPEG_QUALITY, 80])
        if not success:
            continue

        payload = encoded.tobytes()
        header = struct.pack(">Q", len(payload))   # 8-byte big-endian length
        client_socket.sendall(header + payload)

        cv2.imshow("Client Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    camera.release()
    client_socket.close()
    cv2.destroyAllWindows()
    print("Client stopped.")