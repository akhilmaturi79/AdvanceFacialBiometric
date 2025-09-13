from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk      # pip install pillow
import mysql.connector
import os
from time import strftime
from datetime import datetime
from student import Student
from train import Train
from face_recognition import Face_Recognition
from attendance import Attendance
from developer import Developer
from help import Help
from main import Face_Recognition_System

def main():
    win=Tk()
    app=Login_Window(win)
    win.mainloop()


class Login_Window:
    def __init__(self,root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1550x800+0+0")
        self.root.wm_iconbitmap("face.ico")


        self.bg = ImageTk.PhotoImage(file="face_recognition system/college_images/un.jpg")
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        frame=Frame(self.root, bg="black")
        frame.place(x=610, y=200, width=340, height=430)

        img1 = Image.open("face_recognition system/college_images/LoginIconAppl.png")
        img1 = img1.resize((90, 90), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        lblimg1 = Label(image=self.photoimg1, bg="black", borderwidth=0)
        lblimg1.place(x=730, y=200, width=90, height=90)

        get_str = Label(frame, text="Get Started", font=("times new roman", 20, "bold"), fg="white", bg="black")
        get_str.place(x=95, y=85)

        # Label
        username=lb1 = Label(frame, text="Username", font=("times new roman", 12, "bold"), fg="white", bg="black")
        username.place(x=70, y=125)

        self.txtuser=StringVar()
        self.txtpass=StringVar()

        txtuser = ttk.Entry(frame,textvariable=self.txtuser, font=("times new roman", 15, "bold"))
        txtuser.place(x=40, y=150, width=270)

        password=lb1 = Label(frame, text="Password", font=("times new roman", 12, "bold"), fg="white", bg="black")
        password.place(x=70, y=195)

        txtpass = ttk.Entry(frame, textvariable=self.txtpass, font=("times new roman", 15, "bold"), show="*")
        txtpass.place(x=40, y=220, width=270)
    
        # ===================icon Images=================
        img2 = Image.open("face_recognition system/college_images/LoginIconAppl.png")
        img2 = img2.resize((25, 25), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        lblimg2 = Label(image=self.photoimg2, bg="black", borderwidth=0) 
        lblimg2.place(x=650, y=323, width=25, height=25)


        img3 = Image.open("face_recognition system/college_images/lock-512.png")
        img3 = img3.resize((25, 25), Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        lblimg3 = Label(image=self.photoimg3, bg="black", borderwidth=0)
        lblimg3.place(x=650, y=395, width=25, height=25)

        # ===================Login Button=================
        loginbtn = Button(frame,command=self.login, text="Login",borderwidth=3,relief=RAISED,cursor="hand2",font=("times new roman", 15, "bold"),bd=3,fg="white", bg="red", activeforeground="white", activebackground="red")
        loginbtn.place(x=110, y=270, width=120, height=35)

        #===================Register Button=================
        registerbtn = Button(frame, text="Don't have an account? SIGN UP ",command=self.register_window, font=("times new roman", 10, "bold"), borderwidth=0,fg="white", bg="black", activeforeground="white", activebackground="black")
        registerbtn.place(x=37, y=320, width=180)

        #===================forgetpassbtn=================
        forgetbtn = Button(frame, text="Forget Password",command=self.forgot_password_window,font=("times new roman", 10, "bold"), borderwidth=0,fg="white", bg="black", activeforeground="white", activebackground="black")
        forgetbtn.place(x=15, y=340, width=140)
    
    def register_window(self):
        self.new_window=Toplevel(self.root)
        self.app=Register(self.new_window)


    def login(self):
        if self.txtuser.get() == "" or self.txtpass.get() == "":
            messagebox.showerror("Error", "All fields are required")
        elif self.txtuser.get() == "dinesh" and self.txtpass.get() == "8236":
            messagebox.showinfo("Success", "Welcome to the application")
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="Dinesh184@",database="face_recognizer")
            my_cursor=conn.cursor()
            my_cursor.execute("select * from register where email=%s and password=%s",(
                                                                         self.txtuser.get(),
                                                                         self.txtpass.get()
                                                                 ))
            row=my_cursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Invalid Username or Password")
            else:
                open_main=messagebox.askyesno("YesNo","Acess only Authorized Person",parent=self.root)
                if open_main>0:
                    self.new_window = Toplevel(self.root)
                    self.app=Face_Recognition_System(self.new_window)
                else:
                    if not open_main:
                        return
            conn.commit()
            conn.close()

    #=========================================reset password==========================
    def reset_pass(self):
        if self.combo_security_Q.get() == "Select":
            messagebox.showerror("Error","Select security Question",parent=self.root2)
        elif self.txt_security.get()=="":
            messagebox.showerror("Error","Please enter security answer",parent=self.root2)
        elif self.txt_newpass.get()=="":
            messagebox.showerror("Error","Please enter new password",parent=self.root2)
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="Dinesh184@",database="face_recognizer")
            my_cursor=conn.cursor()
            query=("select * from register where email=%s and securityQ=%s and securityA=%s")
            value=(self.txtuser.get(),self.combo_security_Q.get(),self.txt_security.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Please enter valid security answer",parent=self.root2) 
            else:
                query=("update register set password=%s where email=%s")
                value=(self.txt_newpass.get(),self.txtuser.get())
                my_cursor.execute(query,value)

                conn.commit()
                conn.close()
                messagebox.showinfo("Success","Awesome,you've successfully updated your password.",parent=self.root2)
                self.root2.destroy()
                




    #====================================forget password window===========================
    def forgot_password_window(self):
        if self.txtuser.get()=="":
            messagebox.showerror("Error","Please enter your email address to reset your password")
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="Dinesh184@",database="face_recognizer")
            my_cursor=conn.cursor()
            query=("select * from register where email=%s")
            value=(self.txtuser.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            #print(row)

            if row==None:
                messagebox.showerror("Error","Please enter valid email address")
            else:
                conn.close()
                self.root2=Toplevel()
                self.root2.title("Forget Password")
                self.root2.geometry("340x450+610+170")

                l=bl=Label(self.root2,text="Forget Password",font=("times new roman",20,"bold"),fg="red",bg="white")
                l.place(x=0,y=10,relwidth=1)

                security_Q=Label(self.root2,text="Select Security Question",font=("times new roman",15,"bold"),bg="white",fg="black")
                security_Q.place(x=50,y=80)

                self.combo_security_Q = ttk.Combobox(self.root2,font=("times new roman",15,"bold"),state="readonly")
                self.combo_security_Q["values"]=("Select","Your Birth Place","Your First School","Your Pet Name")
                self.combo_security_Q.place(x=50,y=110,width=250)
                self.combo_security_Q.current(0)

                security_A=Label(self.root2,text="Security Answer",font=("times new roman",15,"bold"),bg="white",fg="black")
                security_A.place(x=50,y=150)

                self.txt_security=ttk.Entry(self.root2,font=("times new roman",15,"bold"))
                self.txt_security.place(x=50,y=180,width=250)


                new_password=Label(self.root2,text="New Password",font=("times new roman",15,"bold"),bg="white",fg="black")
                new_password.place(x=50,y=220)

                self.txt_newpass=ttk.Entry(self.root2,font=("times new roman",15,"bold"))
                self.txt_newpass.place(x=50,y=250,width=250)

                btn=Button(self.root2,text="Reset",command=self.reset_pass,font=("times new roman",15,"bold"),bg="green",fg="white")
                btn.place(x=130,y=290)






class Register:
    def __init__(self,root):
        self.root = root
        self.root.title("Register")
        self.root.geometry("1600x900+0+0")


        #===============variables================
        self.var_fname=StringVar()
        self.var_lname=StringVar()
        self.var_contact=StringVar()
        self.var_email=StringVar()
        self.var_securityQ=StringVar()
        self.var_SecurityA=StringVar()
        self.var_pass=StringVar()
        self.var_confpass=StringVar()


        #============== bg image===============
        self.bg = ImageTk.PhotoImage(file="face_recognition system/college_images/un.jpg")
        bg_lbl = Label(self.root, image=self.bg)
        bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)


        #============== left image===============
        self.bg1 = ImageTk.PhotoImage(file="face_recognition system/college_images/thought-good-morning-messages-LoveSove.jpg")
        left_lbl = Label(self.root, image=self.bg1)
        left_lbl.place(x=50, y=100, width=470, height=550)

        #===============main frame===============
        frame = Frame(self.root,bg="white")
        frame.place(x=520,y=100,width=800,height=550)

        register_lb1=Label(frame,text="REGISTER HERE",font=("times new roman",20,"bold"),fg="darkgreen",bg="white")
        register_lb1.place(x=20,y=20)

        #=============label and entry============

        #--------------row1
        fname=Label(frame,text="First Name",font=("times new roman",15,"bold"),bg="white")
        fname.place(x=50,y=100)

        self.fname_entry=ttk.Entry(frame,textvariable=self.var_fname,font=("times new roman",15))
        self.fname_entry.place(x=50,y=130,width=250)

        l_name=Label(frame,text="Last Name",font=("times new roman",15,"bold"),bg="white",fg="black")
        l_name.place(x=370,y=100)

        self.txt_lname=ttk.Entry(frame,textvariable=self.var_lname,font=("times new roman",15))
        self.txt_lname.place(x=370,y=130,width=250)

        #-------------row2

        contact=Label(frame,text="Contact No",font=("times new roman",15,"bold"),bg="white",fg="black")
        contact.place(x=50,y=170)

        self.txt_contact=ttk.Entry(frame,textvariable=self.var_contact,font=("times new roman",15))
        self.txt_contact.place(x=50,y=200,width=250)

        email=Label(frame,text="Email",font=("times new roman",15,"bold"),bg="white",fg="black")
        email.place(x=370,y=170)

        self.txt_email=ttk.Entry(frame,textvariable=self.var_email,font=("times new roman",15))
        self.txt_email.place(x=370,y=200,width=250)

        #-------------row3

        security_Q=Label(frame,text="Select Security Question",font=("times new roman",15,"bold"),bg="white",fg="black")
        security_Q.place(x=50,y=240)

        self.combo_security_Q = ttk.Combobox(frame,textvariable=self.var_securityQ,font=("times new roman",15,"bold"),state="readonly")
        self.combo_security_Q["values"]=("Select","Your Birth Place","Your First School","Your Pet Name")
        self.combo_security_Q.place(x=50,y=270,width=250)
        self.combo_security_Q.current(0)

        security_A=Label(frame,text="Security Answer",font=("times new roman",15,"bold"),bg="white",fg="black")
        security_A.place(x=370,y=240)

        self.txt_security=ttk.Entry(frame,textvariable=self.var_SecurityA,font=("times new roman",15,"bold"))
        self.txt_security.place(x=370,y=270,width=250)


        #--------------row4

        pswd=Label(frame,text="Password",font=("times new roman",15,"bold"),bg="white",fg="black")
        pswd.place(x=50,y=310)

        self.txt_pswd=ttk.Entry(frame,textvariable=self.var_pass,font=("times new roman",15),show="*")
        self.txt_pswd.place(x=50,y=340,width=250)

        confirm_pswd=Label(frame,text="Confirm Password",font=("times new roman",15,"bold"),bg="white",fg="black")
        confirm_pswd.place(x=370,y=310)

        self.txt_confirm_pswd=ttk.Entry(frame,textvariable=self.var_confpass,font=("times new roman",15),show="*")
        self.txt_confirm_pswd.place(x=370,y=340,width=250)

        #======================checkbutton============
        self.var_check=IntVar()
        self.checkbtn=Checkbutton(frame,variable=self.var_check,text="I Agree The Terms & Conditions",font=("times new roman",12,"bold"),onvalue=1,offvalue=0)
        self.checkbtn.place(x=50,y=380)


        #=================buttons===================
        img=Image.open("face_recognition system/college_images/register-now-button1.jpg")
        img=img.resize((150,50),Image.LANCZOS)
        self.photoimage=ImageTk.PhotoImage(img)
        b1=Button(frame,image=self.photoimage,command=self.register_data,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold"),fg="white")
        b1.place(x=50,y=420,width=150)


        img1=Image.open("face_recognition system/college_images/loginpng.png")
        img1=img1.resize((150,45),Image.LANCZOS)
        self.photoimage1=ImageTk.PhotoImage(img1)
        b1=Button(frame,image=self.photoimage1,command=self.login,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold"))
        b1.place(x=370,y=425,width=150)



        #=================function declaration===================

    def register_data(self):
        if self.var_fname.get()=="" or self.var_email.get()=="" or self.var_securityQ.get()=="Select" :
            messagebox.showerror("Error","All fields are required",parent=self.root)
        elif self.var_pass.get() != self.var_confpass.get():
            messagebox.showerror("Error","Password and Confirm Password should be same")
        elif self.var_check.get()==0:
            messagebox.showerror("Error","Please agree our terms and conditions")
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="Dinesh184@",database="face_recognizer")
            my_cursor=conn.cursor()
            query=("select * from register where email=%s")
            value=(self.var_email.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row!=None:
                messagebox.showerror("Error","User already exists, please try another email",parent=self.root)
            else:
                my_cursor.execute("insert into register  values(%s,%s,%s,%s,%s,%s,%s)",
                                    (self.var_fname.get(),
                                     self.var_lname.get(),
                                     self.var_contact.get(),
                                     self.var_email.get(),
                                     self.var_securityQ.get(),
                                     self.var_SecurityA.get(),
                                     self.var_pass.get()
                                        ))
                
                conn.commit()
                conn.close()
                messagebox.showinfo("Success","Registration Successful",parent=self.root)


    def login(self):
        self.root.destroy()

        
class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        
       # first image
        img=Image.open(r"face_recognition system/college_images/Stanford.jpg")
        img=img.resize((500, 130), Image.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)
        
        f_lb1 = Label(self.root, image=self.photoimg)
        f_lb1.place(x=0, y=0, width=500, height=130)
        

       #second image
        img1=Image.open(r"face_recognition system/college_images/facialrecognition.png")
        img1=img1.resize((500, 130), Image.LANCZOS)
        self.photoimg1=ImageTk.PhotoImage(img1)
        
        f_lb1 = Label(self.root, image=self.photoimg1)
        f_lb1.place(x=500, y=0, width=500, height=130)
        
        #third image
        img2=Image.open(r"face_recognition system/college_images/u.jpg")
        img2=img2.resize((500, 130), Image.LANCZOS)
        self.photoimg2=ImageTk.PhotoImage(img2)
        
        f_lb1 = Label(self.root, image=self.photoimg2)
        f_lb1.place(x=1000, y=0, width=580, height=130)

        #bg image
        img3=Image.open(r"face_recognition system/college_images/wp2551980.jpg")
        img3=img3.resize((1530, 730), Image.LANCZOS)
        self.photoimg3=ImageTk.PhotoImage(img3)
        
        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=130, width=1530, height=710)

        
        title_lb1=Label(bg_img,text="FACE RECOGNITION ATTENDENCE SYSTEM SOFTWARE",font=("times new roman",35,"bold"),bg="white",fg="red")
        title_lb1.place(x=0,y=0,width=1530,height=45)

        # ==================time=========================
        def time():
            string = strftime('%H:%M:%S %p')
            lb1.config(text = string)
            lb1.after(1000, time)

        lb1 = Label(title_lb1,font = ('times new roman',14,"bold"),background="white",fg="blue")
        lb1.place(x=0,y=0,width=110,height=50)
        time()
 
        #student button
        img4=Image.open(r"face_recognition system/college_images/smart-attendance.jpg")
        img4=img4.resize((220, 220), Image.LANCZOS)
        self.photoimg4=ImageTk.PhotoImage(img4)
        
        b1=Button(bg_img,image=self.photoimg4,command=self.student_details,cursor="hand2")
        b1.place(x=200,y=100,width=220,height=220)

        b1_1=Button(bg_img,text="Student Details",command=self.student_details,cursor="hand2",font=("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=200,y=300,width=220,height=40)

        #detect face button
        img5=Image.open(r"face_recognition system/college_images/face_detector1.jpg")
        img5=img5.resize((220, 220), Image.LANCZOS)
        self.photoimg5=ImageTk.PhotoImage(img5)
        
        b1=Button(bg_img,image=self.photoimg5,cursor="hand2",command=self.face_data)
        b1.place(x=500,y=100,width=220,height=220)

        b1_1=Button(bg_img,text="FACE Detector",cursor="hand2",command=self.face_data,font=("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=500,y=300,width=220,height=40)

        
        #attendence face button
        img6=Image.open(r"face_recognition system/college_images/report.jpg")
        img6=img6.resize((220, 220), Image.LANCZOS)
        self.photoimg6=ImageTk.PhotoImage(img6)
        
        b1=Button(bg_img,image=self.photoimg6,cursor="hand2",command=self.attendance_data)
        b1.place(x=800,y=100,width=220,height=220)

        b1_1=Button(bg_img,text="Attendence",cursor="hand2",command=self.attendance_data,font=("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=800,y=300,width=220,height=40)

        #Help face button
        img7=Image.open(r"face_recognition system/college_images/help-desk-customer-care-team-icon-blue-square-button-isolated-reflected-abstract-illustration-89657179.jpg")
        img7=img7.resize((220, 220), Image.LANCZOS)
        self.photoimg7=ImageTk.PhotoImage(img7)
        
        b1=Button(bg_img,image=self.photoimg7,cursor="hand2",command=self.help_data)
        b1.place(x=1100,y=100,width=220,height=220)

        b1_1=Button(bg_img,text="Help Desk",cursor="hand2",command=self.help_data,font=("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=1100,y=300,width=220,height=40)

        
        # Train face button
        img8=Image.open(r"face_recognition system/college_images/Train.jpg")
        img8=img8.resize((220, 220), Image.LANCZOS)
        self.photoimg8=ImageTk.PhotoImage(img8)
        
        b1=Button(bg_img,image=self.photoimg8,cursor="hand2",command=self.train_data)
        b1.place(x=200,y=380,width=220,height=220)

        b1_1=Button(bg_img,text="Train Data",cursor="hand2",command=self.train_data,font=("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=200,y=580,width=220,height=40)

        
         # Photos face button
        img9=Image.open(r"face_recognition system/college_images/opencv_face_reco_more_data.jpg")
        img9=img9.resize((220, 220), Image.LANCZOS)
        self.photoimg9=ImageTk.PhotoImage(img9)
        
        b1=Button(bg_img,image=self.photoimg9,cursor="hand2",command=self.open_img)
        b1.place(x=500,y=380,width=220,height=220)

        b1_1=Button(bg_img,text="Photos",cursor="hand2",command=self.open_img,font=("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=500,y=580,width=220,height=40)
        
          #developer face button
        img10=Image.open(r"face_recognition system/college_images/Team-Management-Software-Development.jpg")
        img10=img10.resize((220, 220), Image.LANCZOS)
        self.photoimg10=ImageTk.PhotoImage(img10)
        
        b1=Button(bg_img,image=self.photoimg10,cursor="hand2",command=self.developer_data)
        b1.place(x=800,y=380,width=220,height=220)

        b1_1=Button(bg_img,text="Developer",cursor="hand2",command=self.developer_data,font=("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=800,y=580,width=220,height=40)
        

         # Exit face button
        img11=Image.open(r"face_recognition system/college_images/exit.jpg")
        img11=img11.resize((220, 220), Image.LANCZOS)
        self.photoimg11=ImageTk.PhotoImage(img11)
        
        b1=Button(bg_img,image=self.photoimg11,cursor="hand2",command=self.iExit)
        b1.place(x=1100,y=380,width=220,height=220)

        b1_1=Button(bg_img,text="Exit",cursor="hand2",command=self.iExit,font=("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=1100,y=580,width=220,height=40)
    
    def open_img(self):
        os.startfile("data")

    def iExit(self):
        self.iExit=messagebox.askyesno("Face Recognition","Are you sure you want to exit this project",parent=self.root)
        if self.iExit > 0 :
            self.root.destroy()
        else:
            return





#==================Functions buttons======================
    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)


    def train_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)

    def face_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition(self.new_window)

    def attendance_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)


    def developer_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Developer(self.new_window)


    def help_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Help(self.new_window)



if __name__ == "__main__":
    main()
    


