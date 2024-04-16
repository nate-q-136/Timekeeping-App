from tkinter import Button, Label, E,  Entry, messagebox
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import uuid
from detection.face import FaceDetector
from utils.drawing import ImageDrawing
import os
import numpy as np

os.makedirs("captured_images", exist_ok=True)

class TimeKeepingApp:
    def __init__(self, window:tk.Tk, window_title, window_size="800x800"):
        self.window = window
        self.window.title(window_title)
        self.window.geometry(window_size)

        # Khởi tạo camera
        self.camera = cv2.VideoCapture(0)
        
        # Thông báo
        self.label = tk.Label(window, text="Chấm công", font=("Arial", 16))
        self.label.pack()

        self.label_info = tk.Label(window, text="", font=("Arial", 12))
        self.label_info.place(x=400, y=700)

        # Hiển thị camera
        self.canvas_width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.canvas_height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.aspect_ratio = self.canvas_width / self.canvas_height
        
        # Resize hình ảnh camera để phù hợp với kích thước 800x800
        if self.canvas_width > 800 or self.canvas_height > 800:
            if self.canvas_width >= self.canvas_height:
                self.canvas_width = 800
                self.canvas_height = int(self.canvas_width / self.aspect_ratio)
            else:
                self.canvas_height = 800
                self.canvas_width = int(self.canvas_height * self.aspect_ratio)

        self.canvas = tk.Canvas(window, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # Nút bấm
        self.btn_start_camera = Button(window, text="Start Camera", width=20, command=self.start_camera)
        self.btn_start_camera.place(x=20, y=20)  # Đặt ở tọa độ (20, 20)

        self.btn_stop_camera = Button(window, text="Stop Camera", width=20, command=self.stop_camera)
        self.btn_stop_camera.place(x=760, y=20)  # Đặt ở tọa độ (760, 20)

        self.btn_capture = Button(window, text='Capture Image', width=20, command=self.capture_image)
        self.btn_capture.place(x=20, y=50)  # Đặt ở tọa độ (20, 50)

        self.btn_checkin = Button(window, text="Checkin", width=20, command=self.checkin)   
        self.btn_checkin.place(x=20, y=760)  # Đặt ở tọa độ (760, 50)

        self.btn_checkout = Button(window, text="Checkout", width=20, command=self.checkout)
        self.btn_checkout.place(x=760, y=760)  # Đặt ở tọa độ (760, 50)

        self.btn_register = Button(window, text="Register", width=20, command=self.show_form_register)
        self.btn_register.place(x=400, y=760)  # Đặt ở tọa độ (760, 50)
        # Biến kiểm soát camera
        self.is_camera_running = False

        global captured_image

        # Khởi tạo vòng lặp chạy
        self.update()
        
        # Gọi sự kiện khi đóng cửa số 
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_camera(self):
        self.is_camera_running = True   

    def stop_camera(self):
        self.is_camera_running = False

    def capture_image(self):
        global captured_image
        if captured_image.any():
            # Lưu ảnh
            image_path = f"captured_images/{uuid.uuid4()}.jpg"
            cv2.imwrite(image_path, captured_image)
            print(f"Saved image to {image_path}")
    
    def show_form_register(self):
        form = tk.Toplevel(self.window)
        form.title("Information Form")
        form.geometry("300x150")
        
        # Labels and Entries
        label_name = Label(form, text="Name:")
        label_name.grid(row=0, column=0, padx=5, pady=5)
        entry_name = Entry(form)
        entry_name.grid(row=0, column=1, padx=5, pady=5)
        
        label_id = Label(form, text="ID:")
        label_id.grid(row=1, column=0, padx=5, pady=5)
        entry_id = Entry(form)
        entry_id.grid(row=1, column=1, padx=5, pady=5)
        
        # Buttons
        btn_ok = Button(form, text="OK", command=form.destroy)
        btn_ok.grid(row=2, column=0, padx=5, pady=5)
        
        btn_cancel = Button(form, text="Cancel", command=form.destroy)
        btn_cancel.grid(row=2, column=1, padx=5, pady=5)
    
    def checkin(self):
        print("Checkin")

    def checkout(self):
        print("Checkout")

    

    def update(self):
        global captured_image
        if self.is_camera_running:
            ret, frame = self.camera.read()
            if ret:
                # Resize frame từ camera
                frame:np.ndarray = cv2.resize(frame, (self.canvas_width, self.canvas_height))
                try:
                    
                    data_faces = FaceDetector.detect_v3(frame)
                    num_faces = len(data_faces)
                    # set label number of faces
                    self.label_info.config(text=f"Chấm công - Số khuôn mặt: {num_faces}")
                    for (x, y, w, h) in data_faces:
                        x1, y1, x2, y2 = x, y, x+w, y+h
                        captured_image = frame[y1:y2, x1:x2].copy()
                        frame = ImageDrawing.draw_rectangle(frame, x1=x1, y1=y1, x2=x2, y2=y2)
                    
                    # Chuyển đổi frame cv2 sang PIL
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(image)
                    image = ImageTk.PhotoImage(image)

                    # Hiển thị hình ảnh trên canvas
                    if hasattr(self, 'canvas'):
                        self.canvas.create_image(0, 0, image=image, anchor=tk.NW)
                        self.canvas.image = image
                except Exception as e:
                    # Chuyển đổi frame cv2 sang PIL
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(image)
                    image = ImageTk.PhotoImage(image)

                    # Hiển thị hình ảnh trên canvas
                    if hasattr(self, 'canvas'):
                        self.canvas.create_image(0, 0, image=image, anchor=tk.NW)
                        self.canvas.image = image
                    pass
            
        self.window.after(5, self.update)
    
    def on_closing(self):
        self.is_camera_running = False
        self.window.destroy()

root = tk.Tk()
app = TimeKeepingApp(root, "Timekeeping App")

root.mainloop()
