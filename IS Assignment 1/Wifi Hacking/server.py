
import socket
import struct
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io
PORT = 5000
class PaintViewer:
 def __init__(self, root):
 self.root = root
 self.root.title("SecurePaint - Viewer Server")
 self.root.geometry("900x700")
 self.server_socket = None
 self.client_socket = None
 self.running = False
 title = tk.Label(
 root,
 text="SECURE PAINT - VIEWER SERVER",
 font=("Arial", 20, "bold")
 )
 title.pack(pady=10)
 self.status = tk.Label(
 root,
 text="Server: STOPPED | Client: DISCONNECTED",
 font=("Arial", 12)
 )
 self.status.pack(pady=5)
 self.canvas = tk.Label(
 root,
 text="Waiting for client...",
 relief="solid",
 bd=2
 )
 self.canvas.pack(
 padx=20,
 pady=20,
 fill="both",
 expand=True
 )
 button_frame = tk.Frame(root)
 button_frame.pack(pady=10)
 self.start_button = tk.Button(
 button_frame,
 text="Start Server",
 width=15,
 command=self.start_server
 )
 self.start_button.grid(row=0, column=0, padx=5)
 self.stop_button = tk.Button(
 button_frame,
 text="Stop Server",
 width=15,
 command=self.stop_server,
 state="disabled"
 )
 self.stop_button.grid(row=0, column=1, padx=5)
 self.root.protocol("WM_DELETE_WINDOW", self.close)
 def start_server(self):
 if self.running:
 return
 try:
 self.server_socket = socket.socket(
 socket.AF_INET,
 socket.SOCK_STREAM
 )
 self.server_socket.setsockopt(
 socket.SOL_SOCKET,
 socket.SO_REUSEADDR,
 1
 )
 self.server_socket.bind(("0.0.0.0", PORT))
 self.server_socket.listen(1)
 self.running = True
 self.status.config(
 text=f"Server: RUNNING on port {PORT} | Client: DISCONNECTED"
 )
 self.start_button.config(state="disabled")
 self.stop_button.config(state="normal")
 threading.Thread(
 target=self.accept_client,
 daemon=
a is None:
 break
 image = Image.open(
 io.BytesIO(frame_data)
 )
 image = image.copy()
 self.root.after(
 0,
 self.display_image,
 image
 )
 except Exception:
 pass
 finally:
 if self.client_socket:
 try:
 self.client_socket.close()
 except:
 pass
 self.client_socket = None
 if self.running:
 self.root.after(
 0,
 lambda: self.status.config(
 text=f"Server: RUNNING | Client: DISCONNECTED"
 )
 )
 def display_image(self, image):
 if not self.running:
 return
 max_width = 820
 max_height = 520
 image.thumbnail(
 (max_width, max_height)
 )
 photo = ImageTk.PhotoImage(image)
 self.canvas.config(
 image=photo,
 text=""
 )
 self.canvas.image = photo
 def stop_server(self):
 self.running = False
 if self.client_socket:
 try:
 self.client_socket.shutdown(
 socket.SHUT_RDWR
 )
 except:
 pass
 try:
 self.client_socket.close()
 except:
 pass
 self.client_socket = None
 if self.server_socket:
 try:
 self.server_socket.close()
 except:
 pass
 self.server_socket = None
 self.status.config(
 text="Server: STOPPED | Client: DISCONNECTED"
 )
 self.start_button.config(
 state="normal"
 )
 self.stop_button.config(
 state="disabled"
 )
 def close(self):
 self.stop_server()
 self.root.destroy()
root = tk.Tk()
app = PaintViewer(root)