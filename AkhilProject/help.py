from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2

class Help:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lb1=Label(self.root,text="Help Desk",font=("times new roman",35,"bold"),bg="white",fg="blue")
        title_lb1.place(x=0,y=0,width=1530,height=45)

        img_top=Image.open(r"face_recognition system/college_images/1_5TRuG7tG0KrZJXKoFtHlSg.jpeg")
        img_top=img_top.resize((1530, 720), Image.LANCZOS)
        self.photoimg_top=ImageTk.PhotoImage(img_top)

        f_lb1=Label(self.root,image=self.photoimg_top)
        f_lb1.place(x=0, y=55, width=1530, height=720)

        dev_label=Label(f_lb1,text="Support:dineshreddy08072603@gmail.com",font=("times new roman",20,"bold"),fg="blue",bg="white")
        dev_label.place(x=520,y=220)
    
        back_btn = Button(self.root, text="Back", command=self.go_back, font=("times new roman", 12, "bold"), bg="blue", fg="white", cursor="hand2")
        back_btn.place(x=1400, y=5, width=100, height=40)
        
        # Help & FAQs Button
        faq_btn = Button(self.root, text="Help & FAQs", command=self.open_faqs, font=("times new roman", 12, "bold"), bg="green", fg="white", cursor="hand2")
        faq_btn.place(x=1250, y=5, width=120, height=40)

    # Function to go back to the main page
    def go_back(self):
        self.root.destroy()
        
     # Function to open FAQs window
    def open_faqs(self):
        help_window = Toplevel(self.root)
        help_window.title("Help & FAQs")
        help_window.geometry("800x600")
        #help_window.config(bg="#f0f0f0")

        # Background Image for FAQs Window
        bg_img = Image.open(r"face_recognition system/college_images/Train.jpg")
        bg_img = bg_img.resize((800, 600), Image.LANCZOS)
        self.photoimg_bg = ImageTk.PhotoImage(bg_img)

        bg_label = Label(help_window, image=self.photoimg_bg)
        bg_label.place(x=0, y=0, width=800, height=600)

        # Add Help Title
        Label(help_window, text="Help & FAQs", font=("Arial", 24, "bold"), bg="#ffffff", fg="black").pack(pady=20)
        

        # Frame for FAQs with Scrollbar
        faq_frame = Frame(help_window, bg="#ffffff",bd=2,relief=RIDGE)
        faq_frame.place(x=50, y=100, width=700, height=400)

        canvas = Canvas(faq_frame, bg="#ffffff")
        scrollbar = Scrollbar(faq_frame, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="#ffffff")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        

        # Bind mouse wheel for dynamic scrolling
        def on_mouse_wheel(event):
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")
        
        canvas.bind_all("<MouseWheel>", on_mouse_wheel)

        # FAQs Dictionary
        faqs = {
            "1. How to register my face?": "Go to 'Student page' in the menu, enter details, and look into the camera.",
            "2. Why is my face not being recognized?": "Ensure proper lighting and remove obstructions like masks or hats.",
            "3. What if the attendance is not marked?": "Check the database and make sure your face is registered correctly.",
            "4. How to delete or update a user?": "Admins can manage users in the 'Admin Panel'.",
            "5. How secure is my facial data?": "Data is encrypted and stored securely in the system.",
            "6. Can I use this system with multiple cameras?": "Currently, the system supports a single camera. Multi-camera support can be added in future updates.",
            "7. What happens if two faces are detected at the same time?": "The system processes one face at a time. Ensure only one person is in front of the camera during recognition.",
            "8. How can I reset my data?": "Admins can reset or delete data from the 'Admin Panel' or database directly.",
            "9. What is the accuracy of face recognition?": "The accuracy depends on lighting, camera quality, and the training dataset. Ensure proper conditions for best results.",
            "10. Can I export attendance records?": "Yes, you can export attendance records as a CSV file from the 'Attendance' section.",
            "11. How do I train the system with new faces?": "Go to the 'Train Data' section and click on 'Train Data' to update the system with new faces.",
            "12. What should I do if the system crashes?": "Check the logs for errors, ensure all dependencies are installed, and restart the application.",
            "13. Can I integrate this system with other software?": "Yes, the system can be integrated with other software using APIs or database connections.",
            "14. How do I update the software?": "Download the latest version from the official repository and replace the existing files.",
            "15. What are the hardware requirements?": "A computer with a webcam, at least 4GB RAM, and a dual-core processor is recommended.",
            "16. Can I use this system on a mobile device?": "Currently, the system is designed for desktop use. A mobile version is under development.",
            "17. How do I troubleshoot database connection issues?": "Ensure the database server is running, and the credentials in the code are correct.",
            "18. What is the purpose of the 'Developer' section?": "The 'Developer' section provides information about the project creator and future updates.",
            "19. How do I contact support?": "You can contact support via the email provided on the 'Help Desk' page.",
            "20. Can I customize the system for my organization?": "Yes, the system can be customized. Contact the developer for more details."
        }

        # Display FAQs
        for question, answer in faqs.items():
            Label(scrollable_frame, text=question, font=("Arial", 12, "bold"), bg="#ffffff", fg="black").pack(anchor="w", padx=20, pady=5)
            Label(scrollable_frame, text=answer, wraplength=650, justify="left", bg="#ffffff", fg="gray").pack(anchor="w", padx=40, pady=5)

        
         # Close Button
        Button(help_window, text="Close", command=help_window.destroy, font=("Arial", 12, "bold"), bg="red", fg="white").place(x=350, y=520, width=100, height=40)

if __name__== "__main__":
     root = Tk()
     obj = Help(root)
     root.mainloop()