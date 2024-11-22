import customtkinter as ctk
from PIL import Image, ImageTk

class FaceRecognitionApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.app = ctk.CTk()
        
        width, height = 1300, 600
        
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.app.geometry(f'{width}x{height}+{x}+{y}')
        self.app.resizable(width=False, height=False)
        
        self.app.iconbitmap("images/logo_icon.ico")
        self.app.title("Face Recognition Attendant System")
        
        self.setup_ui()
    def setup_ui(self):

        self.app.grid_rowconfigure(0, weight = 1)
        self.app.grid_columnconfigure(0, weight = 2) 
        self.app.grid_columnconfigure(1, weight = 1)  

        image = Image.open("images/Face_Background.jpg")  
        image = image.resize((1230, 750)) 
        img_tk = ImageTk.PhotoImage(image)  

        left_frame = ctk.CTkFrame(self.app, fg_color = "#2C3E50")
        left_frame.grid(row=0, column=0, sticky="nsew")

        canvas = ctk.CTkCanvas(left_frame, 
                               bg = "#2C3E50", 
                               width = 900, 
                               bd = 0, 
                               highlightthickness = 0)
        canvas.pack(fill = "both", expand = True)
        
        # Place the image on the canvas
        canvas.create_image(0, 0, image = img_tk, anchor = "nw")
        canvas.create_text(1073, 50, 
                           text = "Face Rec", 
                           font = ("Imprint MT Shadow", 50, "bold", "italic"), 
                           fill = "#A8F0F2")
        canvas.create_text(1030, 130, 
                           text = "Attendant", 
                           font = ("Imprint MT Shadow", 50, "bold", "italic"), 
                           fill = "#A8F0F2")
        
        canvas.image = img_tk

        right_frame = ctk.CTkFrame(self.app,
                                   fg_color = "#0c0c0c")
        right_frame.grid(row = 0, column = 1, sticky = "nsew") 
        
        # Center content in the right frame
        right_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight = 1)  
        right_frame.grid_columnconfigure((0, 1, 2, 3), weight = 1)  
        
        # Title Text
        text_title_1 = ctk.CTkLabel(right_frame, 
                                    text = "ognition", 
                                    font = ("Imprint MT Shadow", 52, "bold", "italic"),
                                    text_color = "#A8F0F2")
        text_title_1.grid(row = 0, column = 0, pady = 10, sticky = "wn")  
        
        text_title_2 = ctk.CTkLabel(right_frame,
                                    text = " System", 
                                    font = ("Imprint MT Shadow", 52, "bold", "italic"),
                                    text_color = "#A8F0F2")
        text_title_2.grid(row = 0, column = 0, pady = 75, sticky = "wn") 


        # Three buttons 
        button1 = ctk.CTkButton(right_frame, 
                                text = "Start Webcam", 
                                font = ("Arial Rounded MT Bold", 16), 
                                fg_color = "#004C6D",
                                text_color = "#87CEEB",
                                hover_color = "#003B53",
                                corner_radius = 15,  
                                border_width = 2, 
                                border_color = "#006D79", 
                                width = 200, 
                                height = 75, 
                                command = self.start_recognition)
        button1.grid(row = 0, column = 0, rowspan = 2, columnspan = 2, pady = 50, sticky = "se")  

        button2 = ctk.CTkButton(right_frame, 
                                text = "View Attendance", 
                                font = ("Arial Rounded MT Bold", 16), 
                                fg_color = "#004C6D",
                                text_color = "#87CEEB",
                                hover_color = "#003B53",
                                corner_radius = 15,  
                                border_width = 2, 
                                border_color = "#006D79", 
                                width = 200, 
                                height = 75)
        button2.grid(row = 1, column = 0, rowspan = 3, columnspan = 2, pady = 110, sticky = "ne")  
        
        button3 = ctk.CTkButton(right_frame, 
                                text = "Exit", 
                                font = ("Arial Rounded MT Bold", 16), 
                                fg_color = "#004C6D",
                                text_color = "#87CEEB",
                                hover_color = "#003B53", 
                                corner_radius = 15, 
                                border_width = 2, 
                                border_color = "#006D79", 
                                width = 200, 
                                height = 75, 
                                command = self.app.quit)
        button3.grid(row = 2, column = 0, rowspan = 4, columnspan = 2, pady = 60, sticky = "se") 

    def start_recognition(self):
        print("Recognition started!")

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    face_recognition_app = FaceRecognitionApp()
    face_recognition_app.run()