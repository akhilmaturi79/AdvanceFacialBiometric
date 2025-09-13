# from tkinter import *
# from tkinter import ttk
# from PIL import Image, ImageTk
# from tkinter import messagebox
# import mysql.connector
# from datetime import datetime
# import cv2
# import numpy as np
# import pyttsx3
# import dlib
# from scipy.spatial import distance
# import threading
# import time


# class Face_Recognition:
#     def __init__(self, root):
#         self.root = root
#         self.root.geometry("1530x790+0+0")
#         self.root.title("Face Recognition Attendance System")
#         self.root.config(bg="white")
        

#         self.engine = pyttsx3.init()
#         self.running = True

#         title_lb1 = Label(self.root, text="FACE RECOGNITION", font=("times new roman", 35, "bold"), bg="white", fg="green")    
#         title_lb1.place(x=0, y=0, width=1530, height=45)

#         self.loading_label = Label(self.root, text="", font=("times new roman", 15, "bold"), bg="white", fg="blue")
#         self.loading_label.place(x=10, y=50, width=300, height=30)

#         img_top = Image.open(r"face_recognition system/college_images/face_detector1.jpg")
#         img_top = img_top.resize((650, 700), Image.LANCZOS)
#         self.photoimg_top = ImageTk.PhotoImage(img_top)
#         f_lb1 = Label(self.root, image=self.photoimg_top)
#         f_lb1.place(x=0, y=55, width=650, height=700)

#         img_bottom = Image.open(r"face_recognition system/college_images/facial_recognition_system_identification_digital_id_security_scanning_thinkstock_858236252_3x3-100740902-large.jpg")
#         img_bottom = img_bottom.resize((950, 700), Image.LANCZOS)
#         self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
#         f_lb1 = Label(self.root, image=self.photoimg_bottom)
#         f_lb1.place(x=650, y=55, width=950, height=700)

#         b1_1 = Button(f_lb1, text="Face Recognition", cursor="hand2", font=("times new roman", 18, "bold"), bg="blue", fg="white", command=self.start_face_recognition_thread)
#         b1_1.place(x=365, y=620, width=200, height=40)

#         back_btn = Button(self.root, text="Back", command=self.go_back, font=("times new roman", 15, "bold"), bg="blue", fg="white", cursor="hand2")
#         back_btn.place(x=1400, y=7, width=90, height=30)

#         self.animating = False

#     def go_back(self):
#         self.root.destroy()

#     def speak(self, text):
#         self.engine.say(text)
#         self.engine.runAndWait()

#     def mark_attendance(self, student_id, roll, name, department):
#         with open("dinesh.csv", "r+", newline="\n") as f:
#             myDataList = f.readlines()
#             name_list = [line.split(",")[0] for line in myDataList]

#             if student_id not in name_list:
#                 now = datetime.now()
#                 date = now.strftime("%d/%m/%Y")
#                 time_str = now.strftime("%H:%M:%S")
#                 f.writelines(f"\n{student_id},{roll},{name},{department},{time_str},{date},Present")

#     def animate_loading(self, idx=0):
#         if self.animating:
#             dots = ["", ".", "..", "..."]
#             self.loading_label.config(text=f"Detecting{dots[idx % len(dots)]}")
#             self.root.after(500, self.animate_loading, idx + 1)
#         else:
#             self.loading_label.config(text="")

#     def start_face_recognition_thread(self):
#         self.animating = True
#         self.animate_loading()
#         thread = threading.Thread(target=self.face_recog)
#         thread.start()

#     def face_recog(self):
#         detector = dlib.get_frontal_face_detector()
#         predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#         def eye_aspect_ratio(eye):
#             A = distance.euclidean(eye[1], eye[5])
#             B = distance.euclidean(eye[2], eye[4])
#             C = distance.euclidean(eye[0], eye[3])
#             return (A + B) / (2.0 * C)

#         BLINK_THRESHOLD = 0.2
#         BLINK_FRAMES = 3
#         REQUIRED_BLINKS = 1

#         faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#         clf = cv2.face.LBPHFaceRecognizer_create()
#         clf.read("classifier.xml")

#         cap = cv2.VideoCapture(0)
#         blink_count = 0
#         liveness_confirmed = False
#         unknown_announced = False
#         known_announced_ids = set()
#         prediction_stability = {}
#         stable_threshold = 3

#         last_recognized_id = None
#         last_recognized_info = None
#         frame_display_count = 0
#         max_display_frames = 5

#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)

#             if len(faces) > 0:
#                 (x, y, w, h) = max(faces, key=lambda item: item[2] * item[3])
#                 face_roi = gray[y:y + h, x:x + w]

#                 if not liveness_confirmed:
#                     landmarks = predictor(gray, dlib.rectangle(x, y, x + w, y + h))
#                     left_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)]
#                     right_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)]
#                     avg_ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0

#                     if avg_ear < BLINK_THRESHOLD:
#                         blink_count += 1
#                     else:
#                         if blink_count >= BLINK_FRAMES:
#                             REQUIRED_BLINKS -= 1
#                             blink_count = 0
#                         if REQUIRED_BLINKS <= 0:
#                             liveness_confirmed = True

#                 if liveness_confirmed:
#                     id, predict = clf.predict(face_roi)
#                     confidence = int((100 * (1 - predict / 300)))

#                     if confidence > 75:
#                         if id not in prediction_stability:
#                             prediction_stability[id] = 1
#                         else:
#                             prediction_stability[id] += 1

#                         if prediction_stability[id] >= stable_threshold:
#                             if id not in known_announced_ids:
#                                 conn = mysql.connector.connect(host="localhost", username="root", password="Dinesh184@", database="face_recognizer")
#                                 cursor = conn.cursor()
#                                 cursor.execute("SELECT Name, Roll, Dep, Student_id FROM student WHERE Student_id=%s", (id,))
#                                 result = cursor.fetchone()
#                                 conn.close()

#                                 if result:
#                                     name, roll, dep, student_id = map(str, result)
#                                     self.mark_attendance(student_id, roll, name, dep)
#                                     self.speak(f"Hello {name}, your attendance has been marked.")
#                                     known_announced_ids.add(id)
#                                     last_recognized_id = id
#                                     last_recognized_info = (x, y, w, h, name, roll, dep, student_id)
#                                     frame_display_count = max_display_frames
#                             else:
#                                 last_recognized_id = id
#                                 last_recognized_info = (x, y, w, h, name, roll, dep, student_id)
#                                 frame_display_count = max_display_frames
#                     else:
#                         if not unknown_announced:
#                             self.speak("Unknown person detected")
#                             unknown_announced = True

#             if frame_display_count > 0 and last_recognized_info:
#                 x, y, w, h, name, roll, dep, student_id = last_recognized_info
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
#                 cv2.putText(frame, f"ID: {student_id}", (x, y - 80), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
#                 cv2.putText(frame, f"Roll: {roll}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
#                 cv2.putText(frame, f"Name: {name}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
#                 cv2.putText(frame, f"Department: {dep}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
#                 frame_display_count -= 1

#             cv2.imshow("Live Detection and Face Recognition", frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         self.animating = False
#         cap.release()
#         cv2.destroyAllWindows()

#         if self.root.winfo_exists():
#             self.root.after(0, lambda: self.loading_label.config(text=""))


# if __name__ == "__main__":
#     root = Tk()
#     obj = Face_Recognition(root)
#     root.mainloop() 








# from tkinter import *
# from tkinter import ttk
# from PIL import Image, ImageTk
# from tkinter import messagebox
# import mysql.connector
# from datetime import datetime
# import cv2
# import numpy as np
# import pyttsx3
# import dlib
# from scipy.spatial import distance
# import threading
# import time


# class Face_Recognition:
#     def __init__(self, root):
#         self.root = root
#         self.root.geometry("1530x790+0+0")
#         self.root.title("Face Recognition Attendance System")
#         self.root.config(bg="white")
        
#         self.engine = pyttsx3.init()
#         self.running = True

#         title_lb1 = Label(self.root, text="FACE RECOGNITION", font=("times new roman", 35, "bold"), bg="white", fg="green")    
#         title_lb1.place(x=0, y=0, width=1530, height=45)

#         self.loading_label = Label(self.root, text="", font=("times new roman", 15, "bold"), bg="white", fg="blue")
#         self.loading_label.place(x=10, y=50, width=300, height=30)

#         img_top = Image.open(r"face_recognition system/college_images/face_detector1.jpg")
#         img_top = img_top.resize((650, 700), Image.LANCZOS)
#         self.photoimg_top = ImageTk.PhotoImage(img_top)
#         f_lb1 = Label(self.root, image=self.photoimg_top)
#         f_lb1.place(x=0, y=55, width=650, height=700)

#         img_bottom = Image.open(r"face_recognition system/college_images/facial_recognition_system_identification_digital_id_security_scanning_thinkstock_858236252_3x3-100740902-large.jpg")
#         img_bottom = img_bottom.resize((950, 700), Image.LANCZOS)
#         self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
#         f_lb1 = Label(self.root, image=self.photoimg_bottom)
#         f_lb1.place(x=650, y=55, width=950, height=700)

#         b1_1 = Button(f_lb1, text="Face Recognition", cursor="hand2", font=("times new roman", 18, "bold"), bg="blue", fg="white", command=self.start_face_recognition_thread)
#         b1_1.place(x=365, y=620, width=200, height=40)

#         back_btn = Button(self.root, text="Back", command=self.go_back, font=("times new roman", 15, "bold"), bg="blue", fg="white", cursor="hand2")
#         back_btn.place(x=1400, y=7, width=90, height=30)

#         self.animating = False

#     def go_back(self):
#         self.root.destroy()

#     def speak(self, text):
#         self.engine.say(text)
#         self.engine.runAndWait()

#     def mark_attendance(self, student_id, roll, name, department):
#         with open("dinesh.csv", "r+", newline="\n") as f:
#             myDataList = f.readlines()
#             name_list = [line.split(",")[0] for line in myDataList]

#             if student_id not in name_list:
#                 now = datetime.now()
#                 date = now.strftime("%d/%m/%Y")
#                 time_str = now.strftime("%H:%M:%S")
#                 f.writelines(f"\n{student_id},{roll},{name},{department},{time_str},{date},Present")

#     def animate_loading(self, idx=0):
#         if self.animating:
#             dots = ["", ".", "..", "..."]
#             self.loading_label.config(text=f"Detecting{dots[idx % len(dots)]}")
#             self.root.after(500, self.animate_loading, idx + 1)
#         else:
#             self.loading_label.config(text="")

#     def start_face_recognition_thread(self):
#         self.animating = True
#         self.animate_loading()
#         thread = threading.Thread(target=self.face_recog)
#         thread.start()

#     def face_recog(self):
#         detector = dlib.get_frontal_face_detector()
#         predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#         def eye_aspect_ratio(eye):
#             A = distance.euclidean(eye[1], eye[5])
#             B = distance.euclidean(eye[2], eye[4])
#             C = distance.euclidean(eye[0], eye[3])
#             return (A + B) / (2.0 * C)

#         BLINK_THRESHOLD = 0.2
#         BLINK_FRAMES = 3

#         faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#         clf = cv2.face.LBPHFaceRecognizer_create()
#         clf.read("classifier.xml")

#         cap = cv2.VideoCapture(0)
#         blink_count = 0
#         required_blinks = 1
#         liveness_confirmed = False
#         unknown_announced = False
#         known_announced_ids = set()
#         prediction_stability = {}
#         stable_threshold = 3

#         last_recognized_info = None

#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)

#             if len(faces) > 0:
#                 (x, y, w, h) = max(faces, key=lambda item: item[2] * item[3])
#                 face_roi = gray[y:y + h, x:x + w]

#                 if not liveness_confirmed:
#                     landmarks = predictor(gray, dlib.rectangle(x, y, x + w, y + h))
#                     left_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)]
#                     right_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)]
#                     avg_ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0

#                     if avg_ear < BLINK_THRESHOLD:
#                         blink_count += 1
#                     else:
#                         if blink_count >= BLINK_FRAMES:
#                             required_blinks -= 1
#                             blink_count = 0
#                         if required_blinks <= 0:
#                             liveness_confirmed = True

#                 if liveness_confirmed:
#                     face_resized = cv2.resize(face_roi, (200, 200))
#                     id, predict = clf.predict(face_resized)

#                     confidence = int((100 * (1 - predict / 300)))

#                     if confidence > 75:
#                         if id not in prediction_stability:
#                             prediction_stability[id] = 1
#                         else:
#                             prediction_stability[id] += 1

#                         if prediction_stability[id] >= stable_threshold:
#                             if id not in known_announced_ids:
#                                 conn = mysql.connector.connect(host="localhost", username="root", password="Dinesh184@", database="face_recognizer")
#                                 cursor = conn.cursor()
#                                 cursor.execute("SELECT Name, Roll, Dep, Student_id FROM student WHERE Student_id=%s", (id,))
#                                 result = cursor.fetchone()
#                                 conn.close()

#                                 if result:
#                                     name, roll, dep, student_id = map(str, result)
#                                     self.mark_attendance(student_id, roll, name, dep)
#                                     self.speak(f"Hello {name}, your attendance has been marked.")
#                                     known_announced_ids.add(id)
#                                     last_recognized_info = (x, y, w, h, name, roll, dep, student_id)
#                             else:
#                                 last_recognized_info = (x, y, w, h, name, roll, dep, student_id)
#                     else:
#                         if not unknown_announced:
#                             self.speak("Unknown person detected")
#                             unknown_announced = True
#             else:
#                 # Reset if no face found
#                 blink_count = 0
#                 liveness_confirmed = False
#                 required_blinks = 1
#                 unknown_announced = False
#                 last_recognized_info = None

#             if last_recognized_info:
#                 x, y, w, h, name, roll, dep, student_id = last_recognized_info
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
#                 cv2.putText(frame, f"ID: {student_id}", (x, y - 80), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
#                 cv2.putText(frame, f"Roll: {roll}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
#                 cv2.putText(frame, f"Name: {name}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
#                 cv2.putText(frame, f"Department: {dep}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)

#             cv2.imshow("Live Detection and Face Recognition", frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         self.animating = False
#         cap.release()
#         cv2.destroyAllWindows()

#         if self.root.winfo_exists():
#             self.root.after(0, lambda: self.loading_label.config(text=""))


# if __name__ == "__main__":
#     root = Tk()
#     obj = Face_Recognition(root)
#     root.mainloop()






from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime
import cv2
import numpy as np
import pyttsx3
import dlib
from scipy.spatial import distance
import threading
import time
import os
import csv

class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition Attendance System")
        self.root.config(bg="white")

        # control flags
        self.running = False      # controls the camera loop
        self.thread = None

        # speech engine (keep single instance)
        self.engine = pyttsx3.init()

        title_lb1 = Label(self.root, text="FACE RECOGNITION",
                          font=("times new roman", 35, "bold"),
                          bg="white", fg="green")
        title_lb1.place(x=0, y=0, width=1530, height=45)

        self.loading_label = Label(self.root, text="", font=("times new roman", 15, "bold"),
                                   bg="white", fg="blue")
        self.loading_label.place(x=10, y=50, width=300, height=30)

        # images — wrap in try/except so missing images don't crash UI
        try:
            img_top = Image.open(r"face_recognition system/college_images/face_detector1.jpg")
            img_top = img_top.resize((650, 700), Image.LANCZOS)
            self.photoimg_top = ImageTk.PhotoImage(img_top)
            lbl_top = Label(self.root, image=self.photoimg_top)
            lbl_top.place(x=0, y=55, width=650, height=700)
        except Exception:
            lbl_top = Label(self.root, bg="grey", text="Image missing")
            lbl_top.place(x=0, y=55, width=650, height=700)

        try:
            img_bottom = Image.open(
                r"face_recognition system/college_images/facial_recognition_system_identification_digital_id_security_scanning_thinkstock_858236252_3x3-100740902-large.jpg")
            img_bottom = img_bottom.resize((950, 700), Image.LANCZOS)
            self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
            lbl_bottom = Label(self.root, image=self.photoimg_bottom)
            lbl_bottom.place(x=650, y=55, width=950, height=700)
        except Exception:
            lbl_bottom = Label(self.root, bg="lightgrey", text="Image missing")
            lbl_bottom.place(x=650, y=55, width=950, height=700)

        # Buttons
        b1_1 = Button(lbl_bottom, text="Face Recognition", cursor="hand2",
                      font=("times new roman", 18, "bold"), bg="blue", fg="white",
                      command=self.start_face_recognition_thread)
        b1_1.place(x=365, y=620, width=200, height=40)

        stop_btn = Button(self.root, text="Stop", command=self.stop_face_recognition,
                          font=("times new roman", 15, "bold"), bg="red", fg="white", cursor="hand2")
        stop_btn.place(x=1250, y=7, width=90, height=30)

        back_btn = Button(self.root, text="Back", command=self.go_back,
                          font=("times new roman", 15, "bold"), bg="blue", fg="white", cursor="hand2")
        back_btn.place(x=1400, y=7, width=90, height=30)

        self.animating = False

        # Ensure attendance file exists with header
        if not os.path.exists("dinesh.csv"):
            with open("dinesh.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Roll", "Name", "Department", "Time", "Date", "Status"])

    def go_back(self):
        # stop camera loop and then close window
        self.stop_face_recognition()
        self.root.destroy()

    def speak_nonblocking(self, text):
        # run speech in a separate thread so UI doesn't hang
        def _speak():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception:
                pass

        t = threading.Thread(target=_speak, daemon=True)
        t.start()

    def mark_attendance(self, student_id, roll, name, department):
        # Append only if not already marked today for that ID
        try:
            now = datetime.now()
            date = now.strftime("%d/%m/%Y")
            time_str = now.strftime("%H:%M:%S")
            rows = []
            if os.path.exists("dinesh.csv"):
                with open("dinesh.csv", "r", newline="", encoding="utf-8") as f:
                    rows = [r.strip().split(",") for r in f.readlines() if r.strip()]
            already = any(r[0] == str(student_id) and r[5] == date for r in rows if len(r) >= 6)
            if not already:
                with open("dinesh.csv", "a", newline="", encoding="utf-8") as f:
                    f.write(f"{student_id},{roll},{name},{department},{time_str},{date},Present\n")
        except Exception as e:
            print("mark_attendance error:", e)

    def animate_loading(self, idx=0):
        if self.animating:
            dots = ["", ".", "..", "..."]
            self.loading_label.config(text=f"Detecting{dots[idx % len(dots)]}")
            self.root.after(500, self.animate_loading, idx + 1)
        else:
            self.loading_label.config(text="")

    def start_face_recognition_thread(self):
        if self.running:
            messagebox.showinfo("Already running", "Face recognition is already running.", parent=self.root)
            return
        # Pre-check required files
        if not os.path.exists("classifier.xml"):
            messagebox.showerror("Missing file", "classifier.xml not found. Train or provide a model.", parent=self.root)
            return
        if not os.path.exists("shape_predictor_68_face_landmarks.dat"):
            messagebox.showerror("Missing file", "shape_predictor_68_face_landmarks.dat not found.", parent=self.root)
            return

        self.animating = True
        self.running = True
        self.animate_loading()
        self.thread = threading.Thread(target=self.face_recog, daemon=True)
        self.thread.start()

    def stop_face_recognition(self):
        # signal loop to stop
        self.running = False
        self.animating = False
        # wait briefly for thread to stop (non-blocking UI)
        # thread is daemon, will exit when main program exits if still alive

    def face_recog(self):
        try:
            # dlib detector & predictor
            detector = dlib.get_frontal_face_detector()
            predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

            def eye_aspect_ratio(eye):
                A = distance.euclidean(eye[1], eye[5])
                B = distance.euclidean(eye[2], eye[4])
                C = distance.euclidean(eye[0], eye[3])
                return (A + B) / (2.0 * C)

            BLINK_THRESHOLD = 0.20
            BLINK_FRAMES = 3

            # Use OpenCV builtin haarcascade path
            faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

            # LBPH recognizer from opencv-contrib
            try:
                clf = cv2.face.LBPHFaceRecognizer_create()
                clf.read("classifier.xml")
            except Exception as e:
                messagebox.showerror("Recognizer error", f"Failed to load classifier.xml: {e}", parent=self.root)
                self.animating = False
                self.running = False
                return

            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) if os.name == 'nt' else cv2.VideoCapture(0)
            if not cap.isOpened():
                messagebox.showerror("Camera error", "Could not open webcam.", parent=self.root)
                self.animating = False
                self.running = False
                return

            blink_count = 0
            required_blinks = 1
            liveness_confirmed = False
            unknown_announced = False
            known_announced_ids = set()
            prediction_stability = {}
            stable_threshold = 3
            last_recognized_info = None

            while self.running:
                ret, frame = cap.read()
                if not ret:
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

                if len(faces) > 0:
                    (x, y, w, h) = max(faces, key=lambda item: item[2] * item[3])
                    # ensure ROI inside frame bounds
                    x1, y1 = max(0, x), max(0, y)
                    x2, y2 = min(frame.shape[1], x + w), min(frame.shape[0], y + h)
                    face_roi = gray[y1:y2, x1:x2]

                    # liveness via blink detection using dlib landmarks
                    if not liveness_confirmed:
                        try:
                            landmarks = predictor(gray, dlib.rectangle(x1, y1, x2, y2))
                            left_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)]
                            right_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)]
                            avg_ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0
                        except Exception:
                            avg_ear = 1.0  # if landmarks fail, consider eyes open

                        if avg_ear < BLINK_THRESHOLD:
                            blink_count += 1
                        else:
                            if blink_count >= BLINK_FRAMES:
                                required_blinks -= 1
                                blink_count = 0
                            if required_blinks <= 0:
                                liveness_confirmed = True

                    if liveness_confirmed and face_roi.size != 0:
                        # Resize to the training size you used
                        try:
                            face_resized = cv2.resize(face_roi, (200, 200))
                            id_predict, predict_score = clf.predict(face_resized)  # predict returns (label, confidence)
                        except Exception:
                            id_predict, predict_score = -1, 999

                        # convert OpenCV LBPH confidence to percentage-ish (lower score = better)
                        try:
                            confidence = int(max(0, min(100, 100 - predict_score)))
                        except Exception:
                            confidence = 0

                        if confidence > 75:
                            # stability accumulation
                            prediction_stability[id_predict] = prediction_stability.get(id_predict, 0) + 1
                            if prediction_stability[id_predict] >= stable_threshold:
                                if id_predict not in known_announced_ids:
                                    try:
                                        conn = mysql.connector.connect(host="localhost", user="root", password="your_password_here", database="face_recognizer")
                                        cursor = conn.cursor()
                                        cursor.execute("SELECT Name, Roll, Dep, Student_id FROM student WHERE Student_id=%s", (id_predict,))
                                        result = cursor.fetchone()
                                        conn.close()
                                    except Exception:
                                        result = None

                                    if result:
                                        name, roll, dep, student_id = map(str, result)
                                        self.mark_attendance(student_id, roll, name, dep)
                                        self.speak_nonblocking(f"Hello {name}, your attendance has been marked.")
                                        known_announced_ids.add(id_predict)
                                        last_recognized_info = (x1, y1, x2 - x1, y2 - y1, name, roll, dep, student_id)
                                else:
                                    # update last info from previous read
                                    last_recognized_info = last_recognized_info or (x1, y1, x2 - x1, y2 - y1, "", "", "", "")
                        else:
                            if not unknown_announced:
                                self.speak_nonblocking("Unknown person detected")
                                unknown_announced = True
                else:
                    # reset liveness & counters when no face
                    blink_count = 0
                    liveness_confirmed = False
                    required_blinks = 1
                    unknown_announced = False
                    prediction_stability.clear()
                    last_recognized_info = None

                # Draw rectangle and info if exists
                if last_recognized_info:
                    x, y, w, h, name, roll, dep, student_id = last_recognized_info
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    cv2.putText(frame, f"ID: {student_id}", (x, y - 80), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(frame, f"Roll: {roll}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(frame, f"Name: {name}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(frame, f"Department: {dep}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)

                cv2.imshow("Live Detection and Face Recognition", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # end loop
            self.animating = False
            self.running = False
            cap.release()
            cv2.destroyAllWindows()
            if self.root.winfo_exists():
                self.root.after(0, lambda: self.loading_label.config(text=""))
        except Exception as e:
            print("face_recog error:", e)
            self.animating = False
            self.running = False

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()
