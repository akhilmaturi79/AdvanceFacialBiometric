from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np

class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lb1=Label(self.root,text="Photo Sample Training",font=("times new roman",35,"bold"),bg="white",fg="red")
        title_lb1.place(x=0,y=0,width=1530,height=45)

        img_top=Image.open(r"face_recognition system/college_images/facialrecognition.png")
        img_top=img_top.resize((1530, 325), Image.LANCZOS)
        self.photoimg_top=ImageTk.PhotoImage(img_top)
        f_lb1=Label(self.root,image=self.photoimg_top)
        f_lb1.place(x=0, y=55, width=1530, height=325)
        

        
#button
        b1_1=Button(self.root,text="TRAIN DATA",command=self.train_classifier,cursor="hand2",font=("times new roman",30,"bold"),bg="red",fg="white")
        b1_1.place(x=0,y=380,width=1530,height=60)


        img_bottom=Image.open(r"face_recognition system/college_images/opencv_face_reco_more_data.jpg")
        img_bottom=img_bottom.resize((1530, 325), Image.LANCZOS)
        self.photoimg_bottom=ImageTk.PhotoImage(img_bottom)
        f_lb1=Label(self.root,image=self.photoimg_bottom)
        f_lb1.place(x=0, y=440, width=1530, height=325)

 

    def train_classifier(self):
        try:
            data_dir = "data"
            
            path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]

            faces = []
            ids = []

            for image in path:
                try:
                    # Ensure the filename follows the expected format
                    id = int(os.path.split(image)[1].split('.')[1])
                    img = Image.open(image).convert('L')  # Gray scale image
                    imageNp = np.array(img, 'uint8')

                    faces.append(imageNp)
                    ids.append(id)
                    cv2.imshow("Training", imageNp)
                    cv2.waitKey(1) == 13
                except (ValueError, IndexError):
                    # Skip files that don't match the expected format
                    continue

            if len(faces) == 0 or len(ids) == 0:
                messagebox.showerror("Error", "No valid training data found! Ensure images are in the correct format.", parent=self.root)
                cv2.destroyAllWindows()
                return

            ids = np.array(ids)

            # ============== Train the classifier and save =========
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.train(faces, ids)
            clf.write("classifier.xml")
            cv2.destroyAllWindows()

            messagebox.showinfo("Result", "Training datasets completed!!", parent=self.root)

        except Exception as e:
            # Handle errors gracefully
            messagebox.showerror("Error", f"An error occurred during training: {str(e)}", parent=self.root)

     

if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()
