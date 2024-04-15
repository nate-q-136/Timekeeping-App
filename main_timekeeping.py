from tkinter import Button, Label, E
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import uuid
from detection.face import FaceDetector
from utils.drawing import ImageDrawing
import os


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
        self.btn_1 = Button(window, text="Start Camera", width=20, command=self.start_camera)
        self.btn_1.pack(side=tk.LEFT, padx=20, pady=20)

        self.btn_2 = Button(window, text="Stop Camera", width=20, command=self.stop_camera)
        self.btn_2.pack(side=tk.RIGHT, padx=20, pady=20)

        # Biến kiểm soát camera
        self.is_camera_running = False

        # Khởi tạo vòng lặp chạy
        self.update()
        
        # Gọi sự kiện khi đóng cửa số 
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_camera(self):
        self.is_camera_running = True   

    def stop_camera(self):
        self.is_camera_running = False

    def update(self):
        if self.is_camera_running:
            ret, frame = self.camera.read()
            if ret:
                # Resize frame từ camera
                frame = cv2.resize(frame, (self.canvas_width, self.canvas_height))
                name_temp_image = f"image_{uuid.uuid4()}.jpg"
                store = "temp_images"
                # get full path store
                full_path_store = os.path.join(os.path.dirname(__file__), store)
                print("full_path_store", full_path_store)
                cv2.imwrite(f"{store}/{name_temp_image}", frame)
                try:
                    
                    data_faces = FaceDetector.detect_v2(frame)
                    print("data_faces", data_faces)
                    # face_detector = FaceDetector(image_path=f"{store}/{name_temp_image}", store=full_path_store)
                    # data_faces = face_detector.detect()
                    for (x, y, w, h) in data_faces:
                        # if data_face:
                            # x1, y1, x2, y2 = data_face["target_x"], data_face["target_y"], data_face["target_x2"], data_face["target_y2"]
                        x1, y1, x2, y2 = x, y, x+w, y+h
                        print("x1, y1, x2, y2", x1, y1, x2, y2)
                        frame = ImageDrawing.draw_rectangle(frame, x1=x1, y1=y1, x2=x2, y2=y2)
                    
                    # Chuyển đổi frame cv2 sang PIL
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(image)
                    image = ImageTk.PhotoImage(image)

                    os.remove(f"{store}/{name_temp_image}")
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
                    os.remove(f"{store}/{name_temp_image}")
                    pass
            
        self.window.after(5, self.update)
    
    def on_closing(self):
        self.is_camera_running = False

root = tk.Tk()
app = TimeKeepingApp(root, "Timekeeping App")

root.mainloop()
