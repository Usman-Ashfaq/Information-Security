import socket
import struct
import threading
import tkinter as tk
from tkinter import messagebox, colorchooser
from PIL import ImageGrab
import time
PORT = 5000
class SecurePaint:
 def __init__(self, root):
 self.root = root
 self.root.title("SecurePaint - Capture Client")
 self.root.geometry("900x700")
 self.socket = None
 self.connected = False
 self.streaming = False
 self.last_x = None
 self.last_y = None
 title = tk.Label(
 root,
 text="SECURE PAINT - CAPTURE CLIENT",
 font=("Arial", 20, "bold")
 )
 title.pack(pady=10)
 top = tk.Frame(root)
 top.pack(pady=5)
 tk.Label(
 top,
 text="Viewer IP:"
 ).grid(row=0, column=0, padx=5)
 self.ip_entry = tk.Entry(
 top,
 width=20
 )
 self.ip_entry.insert(
 0,
 "10.100.8.170"
 )
 self.ip_entry.grid(
 row=0,
 column=1,
 padx=5
 )
 self.connect_button = tk.Button(
 top,
 text="Connect",
 command=self.connect
 )
 self.connect_button.grid(
 row=0,
 column=2,
 padx=5
 )
 self.start_button = tk.Button(
 top,
 text="Start Stream",
 command=self.start_stream,
 state="disabled"
 )
 self.start_button.grid(
 row=0,
 column=3,
 padx=5
 )
 self.stop_button = tk.Button(
 top,
 text="Stop Stream",
 command=self.stop_stream,
 state="disabled"
 )
 self.stop_button.grid(
 row=0,
 column=4,
 padx=5
 )
 tools = tk.Frame(root)
 tools.pack(pady=5)
 tk.Button(
 tools,
 text="Clear",
 command=self.clear_canvas
 ).pack(side="left", padx=5)
 tk.Button(
 tools,
 text="Choose Color",
 command=self.choose_color
).pack(side="left", padx=5)
 tk.Label(
 tools,
 text="Brush Size:"
 ).pack(side="left", padx=5)
 self.size_entry = tk.Entry(
 tools,
 width=5
 )
 self.size_entry.insert(
 0,
 "5"
 )
 self.size_entry.pack(
 side="left"
 )
 self.paint_canvas = tk.Canvas(
 root,
 width=820,
 height=500,
 bg="white",
 cursor="cross"
 )
 self.paint_canvas.pack(
 pady=10
 )
 self.paint_canvas.bind(
 "<Button-1>",
 self.start_draw
 )
 self.paint_canvas.bind(
 "<B1-Motion>",
 self.draw
 )
 self.paint_canvas.bind(
 "<ButtonRelease-1>",
 self.end_draw
 )
 self.status = tk.Label(
 root,
 text="Connection: DISCONNECTED | Stream: STOPPED",
 font=("Arial", 12)
 )
 self.status.pack(pady=5)
 self.root.protocol(
 "WM_DELETE_WINDOW",
 self.close
 )
 def start_draw(self, event):
 self.last_x = event.x
 self.last_y = event.y
 def draw(self, event):
 try:
 size = int(
 self.size_entry.get()
 )
 except:
 size = 5
 if self.last_x is not None:
 self.paint_canvas.create_line(
 self.last_x,
 self.last_y,
 event.x,
 event.y,
 fill=self.color,
 width=size,
 capstyle=tk.ROUND,
 smooth=True
 )
 self.last_x = event.x
 self.last_y = event.y
 def end_draw(self, event):
 self.last_x = None
 self.last_y = None
 def choose_color(self):
 selected = colorchooser.askcolor(
 title="Choose Brush Color"
 )
 if selected[1]:
 self.color = selected[1]
 def clear_canvas(self):
 self.paint_canvas.delete(
 "all"
 )
def connect(self):
 server_ip = self.ip_entry.get().strip()
 try:
 self.socket = socket.socket(
 socket.AF_INET,
 socket.SOCK_STREAM
 )
 self.socket.connect(
 (server_ip, PORT)
 )
 self.connected = True
 self.connect_button.config(
 state="disabled"
 )
 self.start_button.config(
 state="normal"
 )
 self.status.config(
 text="Connection: CONNECTED | Stream: STOPPED"
 )
 messagebox.showinfo(
 "Connected",
 "Successfully connected to the viewer."
 )
 except Exception as e:
 self.socket = None
 messagebox.showerror(
 "Connection Error",
 f"Could not connect to server.\n\n{e}"
 )
 def start_stream(self):
 if not self.connected:
 return
 if self.streaming:
 return
 self.streaming = True
 self.start_button.config(
 state="disabled"
 )
 self.stop_button.config(
 state="normal"
 )
 self.status.config(
 text="Connection: CONNECTED | Stream: LIVE"
 )
 threading.Thread(
 target=self.stream_loop,
 daemon=True
 ).start()
 def stream_loop(self):
 try:
 while self.streaming and self.connected:
 x = self.root.winfo_rootx()
 y = self.root.winfo_rooty()
 width = self.root.winfo_width()
 height = self.root.winfo_height()
 screenshot = ImageGrab.grab(
 bbox=(
 x,
 y,
 x + width,
 y + height
 )
 )
 screenshot.thumbnail(
 (800, 600)
 )
 buffer = __import__(
 "io"
 ).BytesIO()
 screenshot.save(
 buffer,
 format="JPEG",
 quality=65
 )
 frame_data = buffer.getvalue()
header = struct.pack(
 "!I",
 len(frame_data)
 )
 self.socket.sendall(
 header + frame_data
 )
 time.sleep(
 0.08
 )
 except Exception:
 self.connected = False
 self.streaming = False
 self.root.after(
 0,
 lambda: self.status.config(
 text="Connection: DISCONNECTED | Stream: STOPPED"
 )
 )
 def stop_stream(self):
 self.streaming = False
 self.start_button.config(
 state="normal"
 )
 self.stop_button.config(
 state="disabled"
 )
 self.status.config(
 text="Connection: CONNECTED | Stream: STOPPED"
 )
 def close(self):
 self.streaming = False
 self.connected = False
 if self.socket:
 try:
 self.socket.shutdown(
 socket.SHUT_RDWR
 )
 except:
 pass
 try:
 self.socket.close()
 except:
 pass
 self.root.destroy()
root = tk.Tk()
app = SecurePaint(root)
app.color = "black"
root.mainloop()