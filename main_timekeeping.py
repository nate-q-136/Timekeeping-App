from tkinter import Button, Label, E,  Entry, messagebox
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import uuid
from detection.face import FaceDetector
from utils.drawing import ImageDrawing
import os
import numpy as np
from utils.db_image import FaceInfoHelper, TimeKeepingHelper
from utils.handlers import ImageHandler
import time
from datetime import datetime

os.makedirs("captured_images", exist_ok=True)

class TimeKeepingApp:
    def __init__(self, window:tk.Tk, window_title, window_size="800x800"):
        """
        Create a window for timekeeping app with:
        - Start Camera button
        - Stop Camera button
        - Capture Image button
        - Checkin button
        - Checkout button
        - Register button
        - Label to show number of faces
        - Label to show information
        - Canvas to show camera frame
        """
        self.window = window
        self.window.title(window_title)
        self.window.geometry(window_size)

        # Initialize camera
        self.camera = cv2.VideoCapture(0)
        
        # Label title
        self.label = tk.Label(window, text="TimeKeeping", font=("Arial", 16))
        self.label.place(relx=0.5, rely=0.05, anchor='center')  # Đặt ở giữa trên cùng của cửa sổ

        self.label_info = tk.Label(window, text="", font=("Arial", 12))
        self.label_info.place(relx=0.5, rely=0.75, anchor='center')  # Đặt ở giữa dưới cùng của cửa sổ

        # Setting canvas to show camera frame
        self.canvas_width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.canvas_height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.aspect_ratio = self.canvas_width / self.canvas_height
        
        # Resize image that can fit with the window
        if self.canvas_width > 800 or self.canvas_height > 800:
            if self.canvas_width >= self.canvas_height:
                self.canvas_width = 800
                self.canvas_height = int(self.canvas_width / self.aspect_ratio)
            else:
                self.canvas_height = 800
                self.canvas_width = int(self.canvas_height * self.aspect_ratio)

        self.canvas = tk.Canvas(window, width=self.canvas_width, height=self.canvas_height)
        self.canvas.place(relx=0.5, rely=0.4, anchor='center')  # Đặt ở giữa của cửa sổ

        # Settings Buttons
        btn_width = 20
        btn_height = 2

        self.btn_start_camera = Button(window, text="Start Camera", width=btn_width, height=btn_height, command=self.start_camera)
        self.btn_start_camera.place(relx=0.1, rely=0.9, anchor='center')  # Đặt ở góc trái dưới

        self.btn_stop_camera = Button(window, text="Stop Camera", width=btn_width, height=btn_height, command=self.stop_camera)
        self.btn_stop_camera.place(relx=0.9, rely=0.9, anchor='center')  # Đặt ở góc phải dưới

        self.btn_capture = Button(window, text='Capture Image', width=btn_width, height=btn_height, command=self.capture_image)
        self.btn_capture.place(relx=0.5, rely=0.9, anchor='center')  # Đặt ở giữa dưới

        self.btn_checkin = Button(window, text="Checkin", width=btn_width, height=btn_height, command=self.checkin)   
        self.btn_checkin.place(relx=0.1, rely=0.95, anchor='center')  # Đặt ở góc trái dưới

        self.btn_checkout = Button(window, text="Checkout", width=btn_width, height=btn_height, command=self.checkout)
        self.btn_checkout.place(relx=0.9, rely=0.95, anchor='center')  # Đặt ở góc phải dưới

        self.btn_register = Button(window, text="Register", width=btn_width, height=btn_height, command=self.show_form_register)
        self.btn_register.place(relx=0.5, rely=0.95, anchor='center')  # Đặt ở giữa dưới

        # Camera control variables
        self.is_camera_running = False

        global captured_image
        self.list_faces = []

        # Update frame from camera
        self.update()
        
        # Close window event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_camera(self):
        self.is_camera_running = True   

    def stop_camera(self):
        self.is_camera_running = False

    def capture_image(self):
        global captured_image
        if captured_image.any():
            # Save image
            image_path = f"captured_images/{uuid.uuid4()}.jpg"
            cv2.imwrite(image_path, captured_image)
            print(f"Saved image to {image_path}")
    
    def show_form_register(self):
        global captured_image
        if captured_image.any():
            self.is_camera_running = False
            
        form = tk.Toplevel(self.window)
        form.title("Information Form")
        form.geometry("300x150")
        
        # Labels and Entries
        label_name = Label(form, text="Name:")
        label_name.grid(row=0, column=0, padx=5, pady=5)
        entry_name = Entry(form)
        entry_name.grid(row=0, column=1, padx=5, pady=5)
        
        # Buttons pass param to function
        btn_save = Button(form, text="Save", command=lambda: self.save_face_info(entry_name.get(), captured_image, form=form))
        btn_save.grid(row=2, column=0, padx=5, pady=5)
        
        btn_cancel = Button(form, text="Cancel", command=form.destroy)
        btn_cancel.grid(row=2, column=1, padx=5, pady=5)

    def save_face_info(self, entry_name:str, captured_image:np.ndarray, form:tk.Toplevel):
        FaceInfoHelper().insert_record(entry_name, captured_image)
        messagebox.showinfo("Information", "Saved successfully!")
        form.destroy()
        
    
    def checkin(self):
        print("Checkin")
        global captured_image
        if captured_image.any():
            # Check info person from face image
            id, name, image = ImageHandler().check_info_image(captured_image)
            print("info:", id, name, image.shape)
            if name:
                start_time = time.strftime("%Y-%m-%d %H:%M:%S")

                # insert checkin time
                TimeKeepingHelper().insert_record(id, start_time, None)

                messagebox.showinfo("Information", f"Checkin successfully! Welcome {name}")
            else:
                messagebox.showinfo("Information", "Checkin failed! Please register first")
        else:
            messagebox.showinfo("Information", "Please capture image first")
            

    def checkout(self):
        print("Checkout")
        global captured_image
        if captured_image.any():
            # Check info person from face image
            id, name, image = ImageHandler().check_info_image(captured_image)
            if name:
                end_time = time.strftime("%Y-%m-%d %H:%M:%S")
                # update checkout time
                TimeKeepingHelper().update_checkout_record(id, None, end_time)
                id, name, checkin, checkout = TimeKeepingHelper().get_lastest_checkin_record_by_id(id)
                time_working = datetime.strptime(checkout, "%Y-%m-%d %H:%M:%S") - datetime.strptime(checkin, "%Y-%m-%d %H:%M:%S")
                print("Time working:", time_working)
                hours_time_working = round(time_working.total_seconds() / 3600, 3)
                messagebox.showinfo("Information", f"Checkout successfully! You have worked {hours_time_working} hours today! Goodbye {name}")
            else:
                messagebox.showinfo("Information", "Checkout failed! Please register first")
        else:
            messagebox.showinfo("Information", "Please capture image first")

    def show_frame_on_window(self, frame):
        """
        Convert numpy array image to PIl image and show on window
        """
        # Convert frame with np.ndarray type to PIL Image type
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        # Hiển thị hình ảnh trên canvas
        if hasattr(self, 'canvas'):
            self.canvas.create_image(0, 0, image=image, anchor=tk.NW)
            self.canvas.image = image


    def update(self):
        """
        Update frame from camera and show on window
        """
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
                        id, name, image = ImageHandler().check_info_image(captured_image)
                        frame = ImageDrawing.draw_rectangle(frame,id=id, name=name, x1=x1, y1=y1, x2=x2, y2=y2)
                    
                except Exception as e:
                    pass    
                
                self.show_frame_on_window(frame)    


        self.window.after(5, self.update)
    
    def on_closing(self):
        self.is_camera_running = False
        self.window.destroy()

root = tk.Tk()
app = TimeKeepingApp(root, "Timekeeping App")

root.mainloop()
