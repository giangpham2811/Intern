import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
from keras.models import load_model
# from tensorflow import *
# import tensorflow.compiler.tf2tensorrt.ops.gen_trt_ops
LARGE_FONT = ("Verdana", 35)
MEDIUM_FONT = ("Verdana", 23)
NORMAL_FONT = ("Verdana", 14)


def exit_app():
    response = messagebox.askyesno("Machine Learning App", "Do you want exit")
    if response == 1:
        app.destroy()


class InternApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, ImagePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


def clicked(param):
    print(param)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#F0F8FF")
        label = tk.Label(self, text="Application using Keras Model", font=LARGE_FONT, fg="Blue", bg="#F0F8FF")
        label.pack(padx=10, pady=10)
        button_next = tk.Button(self, text="Next", command=lambda: controller.show_frame(ImagePage))
        button_next.pack()
        button_next2 = tk.Button(self, text="Quit", command=lambda: exit_app())
        button_next2.pack()


class ImagePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#F0F8FF")
        label_title = tk.Label(self, text="About method : ", font=LARGE_FONT, fg="Blue", bg="#F0F8FF")
        label_title.grid(row=0, column=0, padx=10, pady=10)
        label_description = tk.Label(self,
                                     text="Validation is a method to determine and evaluate whether the photos you "
                                          "choose.\n "
                                          " The method will return Good and Fail.\n"
                                          " The method is implemented by Keras and Tensorflow.\n"
                                          " You can open the image and press the Run button to experience.\n",
                                     bg="grey", fg="#E6E6FA")
        label_description.grid(row=0, column=1, padx=10, pady=10, columnspan=4)
        button_load_img = tk.Button(self, text="Open Image", command=self.load_img)
        button_load_img.grid(row=1, column=1)
        button_back = tk.Button(self, text="Back to home", command=lambda: controller.show_frame(StartPage))
        button_back.grid(row=1, column=3)
        button_run = tk.Button(self, text="Run", command=self.run, padx=15, pady=15)
        button_run.grid(row=1, column=4)
        label_guide_text = tk.Label(self, text="Picture Input and Result :", font=MEDIUM_FONT, fg='#00BFFF')
        label_guide_text.grid(row=3, column=0, padx=10, pady=10, columnspan=4)
        image_layer = tk.Frame(self, bg="black", padx=5, pady=5, width=250, height=250)
        image_layer.grid(row=4, column=0)
        label_img = tk.Label(image_layer, bg="#DEE1E6", padx=5, pady=5, text='Image Input')
        label_img.place(relwidth=1, relheight=1)
        self.image_layer = image_layer
        result_layer = tk.Frame(self, bg="black", padx=5, pady=5, width=250, height=250)
        result_layer.grid(row=4, column=4)
        result_label = tk.Label(result_layer, bg="#DEE1E6", padx=5, pady=5, text='Output Result')
        result_label.place(relwidth=1, relheight=1)
        self.result_layer = result_layer
        canvas = tk.Canvas(self, width=100, height=10, bg="#F0F8FF")
        canvas.grid(row=4, column=2)
        canvas.create_line(5, 5, 100, 5, arrow=tk.LAST)

    def load_img(self):
        global img_insert
        global file_name
        file_name = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select A File", filetypes=(
            ("jpg images", ".jpg"), ("png images", ".png"), ("all files", "*.*")))
        img_insert = ImageTk.PhotoImage(Image.open(file_name))
        image_layer = self.image_layer
        label_img = tk.Label(image_layer, image=img_insert, bg="black", text="Image")
        label_img.place(relwidth=1, relheight=1)

    def run(self):
        model = load_model('Model-L502-2.h5')
        model.summary()
        image = cv2.imread(filename=file_name)
        image = cv2.resize(image, (178, 178))
        image = np.array(image)
        image = image.reshape((1, 178, 178, 3))
        predict = model.predict_classes(image)
        result_layer = self.result_layer
        if predict == 1:
            result_label = tk.Label(result_layer, bg="black", text="Your Image is Good", fg="white").place(relwidth=1,
                                                                                                           relheight=1)
        else:
            result_label = tk.Label(result_layer, bg="black", text="Your Image is Bad", fg="white").place(relwidth=1,
                                                                                                          relheight=1)


app = InternApp()
app.title("Machine Learning App")
app.geometry("1000x500")
app.mainloop()
