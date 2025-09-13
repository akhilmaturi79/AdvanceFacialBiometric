from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2

class Developer:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lb1=Label(self.root,text="DEVELOPER INFORMATION",font=("times new roman",35,"bold"),bg="white",fg="blue")
        title_lb1.place(x=0,y=0,width=1530,height=45)

        img_top=Image.open(r"face_recognition system/college_images/dev.jpg")
        img_top=img_top.resize((1530, 730), Image.LANCZOS)
        self.photoimg_top=ImageTk.PhotoImage(img_top)

        f_lb1=Label(self.root,image=self.photoimg_top)
        f_lb1.place(x=0, y=55, width=1530, height=730)


        # Frame
        main_frame=Frame(f_lb1,bd=2,bg="white")
        main_frame.place(x=1000,y=0,width=520,height=725)

        img_top1=Image.open(r"face_recognition system/college_images/dinesh img.jpg")
        img_top1=img_top1.resize((200, 200), Image.LANCZOS)
        self.photoimg_top1=ImageTk.PhotoImage(img_top1)

        f_lb1=Label(main_frame,image=self.photoimg_top1)
        f_lb1.place(x=320, y=0, width=200, height=200)

        # Developer info
        dev_label=Label(main_frame,text="Developer Details",font=("times new roman",18,"bold"),fg="white",bg="blue")
        dev_label.place(x=0,y=5)

        dev_label=Label(main_frame,text="Name: Aindla Dinesh Reddy",font=("times new roman",14),fg="black",bg="white",justify="left")
        dev_label.place(x=0,y=45)

        dev_label3 = Label(main_frame, text="Role: Developer & Designer", font=("times new roman", 14), fg="black", bg="white",justify="left")
        dev_label3.place(x=0, y=80)

        dev_label5 = Label(main_frame, text="Email: dineshreddy08072603@gmail.com", font=("times new roman", 13), fg="black", bg="white",justify="left")
        dev_label5.place(x=0, y=110)
        
        dev_linkedin_label = Label(main_frame, text="LinkedIn: ", font=("times new roman", 14), fg="black", bg="white", justify="left")
        dev_linkedin_label.place(x=0, y=140)

        dev_linkedin_username = Label(main_frame, text="dinesh-reddy-22833a1b5.", font=("times new roman", 14), fg="blue", bg="white", justify="left", cursor="hand2")
        dev_linkedin_username.place(x=80, y=140)
        dev_linkedin_username.bind("<Button-1>", lambda e: self.open_url("https://www.linkedin.com/in/dinesh-reddy-22833a1b5/"))
        
        # About the Project
        project_label = Label(main_frame, text="About the Project", font=("times new roman", 18, "bold"), fg="white", bg="blue")
        project_label.place(x=0, y=175)

        project_name_label = Label(main_frame, text="Project Name : Advanced Facial Biometric Attendance System", font=("times new roman", 14), fg="black", bg="white", justify="left", wraplength=480)
        project_name_label.place(x=0, y=210)

        project_desc_label = Label(main_frame, text="Description : A smart and efficient facial recognition-based attendance system using Python and Tkinter for a user-friendly interface.", font=("times new roman", 14), fg="black", bg="white", justify="left", wraplength=480)
        project_desc_label.place(x=0, y=240)

        project_tech_label = Label(main_frame, text="Technology Stack : Python, OpenCV, Tkinter, MySQL, Machine Learning.", font=("times new roman", 14), fg="black", bg="white", justify="left", wraplength=480)
        project_tech_label.place(x=0, y=310)

    


        # Upcoming Features
        upcoming_features_label = Label(main_frame, text="Upcoming Features", font=("times new roman", 18, "bold"), fg="white", bg="blue")
        upcoming_features_label.place(x=0, y=370)

        feature_1_label = Label(main_frame, text="• AI-Powered Chatbot: A built-in chatbot to assist users with attendance issues, troubleshooting, and general queries.", font=("times new roman", 14), fg="black", bg="white", justify="left", wraplength=480)
        feature_1_label.place(x=0, y=410)

        feature_2_label = Label(main_frame, text="• Cloud Integration: Storing attendance data securely on cloud platforms for remote access.", font=("times new roman", 14), fg="black", bg="white", justify="left", wraplength=480)
        feature_2_label.place(x=0, y=460)

        feature_3_label = Label(main_frame, text="• Mobile App Support: Developing a companion mobile app for attendance tracking and notifications.", font=("times new roman", 14), fg="black", bg="white", justify="left", wraplength=480)
        feature_3_label.place(x=0, y=510)

        































