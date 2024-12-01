import customtkinter as ctk
from PIL import Image, ImageTk
from process_webcam import processing_app
from attendance import get_all_attendance, get_specific_name_and_date, get_specific_name, get_specific_date, initialize

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
        self.app.title("Face Recognition Attendance System")
        
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
                           text = "Attendance", 
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
                                    text = "- System", 
                                    font = ("Imprint MT Shadow", 52, "bold", "italic"),
                                    text_color = "#A8F0F2")
        text_title_2.grid(row = 0, column = 0, pady = 75, sticky = "wn") 

        # Three buttons 
        button1 = ctk.CTkButton(right_frame, 
                                text = "Start Webcam", 
                                font = ("Arial Rounded MT Bold", 17, "bold"), 
                                fg_color = "#004C6D",
                                text_color = "#87CEEB",
                                hover_color = "#003B53",
                                corner_radius = 15,  
                                border_width = 2, 
                                border_color = "#006D79", 
                                width = 200, 
                                height = 75, 
                                command = lambda: self.start_webcam())
        button1.grid(row = 0, column = 0, rowspan = 2, columnspan = 2, pady = 50, sticky = "se")  

        button2 = ctk.CTkButton(right_frame, 
                                text = "View Attendance", 
                                font = ("Arial Rounded MT Bold", 17, "bold"), 
                                fg_color = "#004C6D",
                                text_color = "#87CEEB",
                                hover_color = "#003B53",
                                corner_radius = 15,  
                                border_width = 2, 
                                border_color = "#006D79", 
                                width = 200, 
                                height = 75,
                                command = self.attendance_window)
        button2.grid(row = 1, column = 0, rowspan = 3, columnspan = 2, pady = 110, sticky = "ne")  
        
        button3 = ctk.CTkButton(right_frame, 
                                text = "Exit", 
                                font = ("Arial Rounded MT Bold", 17, "bold"), 
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
        
    def start_webcam(self):
        print("Starting the webcam....")
        try:
            self.app.withdraw()  
            processing_app()  
        except Exception as e:
            print(f"Error in webcam processing: {e}")
        finally:
            self.app.deiconify()
            print("Webcam process finished.")
            
    def set_icon(self, customer_window):
        try:
            customer_window.iconbitmap("images/logo_icon.ico")
        except Exception as e:
            print(f"Error setting icon: {e}")
            
    def attendance_window(self):
        
        self.app.withdraw() 

        # Create a new CTkToplevel window
        customer_window = ctk.CTkToplevel()

        width, height = 720, 500
        screen_width = customer_window.winfo_screenwidth()
        screen_height = customer_window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        # Delay setting the icon for 1000 ms (1 second)
        customer_window.after(1000, self.set_icon, customer_window)  # Delay the icon set by 1 second
        
        customer_window.geometry(f'{width}x{height}+{x}+{y}')
        customer_window.resizable(width=False, height=False)
        customer_window.title("Face Recognition Attedance System")

        # Title bar
        title_frame = ctk.CTkFrame(customer_window, height = 60, corner_radius = 0)
        title_frame.pack(fill = "x", side = "top")
        ctk.CTkLabel(
            title_frame,
            text = "Attendance Management System",
            font = ("Imprint MT Shadow", 30, "bold", "italic"),
            text_color = "white"
        ).pack(pady = 10)

        # Search bar frame
        search_frame = ctk.CTkFrame(customer_window, corner_radius = 10, fg_color = "#2c2c2c")
        search_frame.pack(pady = 20, padx = 20, fill = "x")

        search_entry_name = ctk.CTkEntry(
            search_frame,
            font = ("Times New Roman", 16),
            placeholder_text = "Search by Name",
            width = 250,
            corner_radius = 10
        )
        search_entry_name.pack(side = "left", padx = 10, pady = 10)

        search_entry_date = ctk.CTkEntry(
            search_frame,
            font = ("Times New Roman", 16),
            placeholder_text = "Search by Date (YYYY-MM-DD)",
            width = 250,
            corner_radius = 10
        )
        search_entry_date.pack(side = "left", padx = 10, pady = 10)

        def search_attendance():
            # Get the search parameters
            name = search_entry_name.get()
            date = search_entry_date.get()

            if not name and not date:
                attendance_data = get_all_attendance()  # Default to all data if no filters are set
            elif name and not date:
                attendance_data = get_specific_name(name)  # Filter by name only
            elif not name and date:
                attendance_data = get_specific_date(date)  # Filter by date only
            else:
                attendance_data = get_specific_name_and_date(name, date)  # Filter by both name and date

            # Update the scrollable frame with the filtered attendance data
            update_scrollable_frame(attendance_data)
    
        # Search Button with Icon (Optional)
        search_icon = ctk.CTkImage(
            Image.open("images/search_icon.png"), size = (20, 20)
        )

        search_button = ctk.CTkButton(
            search_frame,
            text = "Search",
            font = ("Arial", 14, "bold"),
            image = search_icon,
            width = 100,
            corner_radius = 10,
            fg_color = "blue",
            hover_color = "lightblue",
            command = search_attendance # Bind the search function to the button
        )
        search_button.pack(pady = 10, padx = 15, anchor = "e")

        # Scrollable frame for attendance data
        scrollable_frame = ctk.CTkScrollableFrame(
            customer_window, width = 950, height = 250, corner_radius = 10, fg_color = "#1e1e1e"
        )
        scrollable_frame.pack(pady = 10, padx = 20, fill = "both", expand = True)
        
        # Configure grid columns for spacing
        scrollable_frame.grid_columnconfigure(0, minsize = 80)  # Column for "No"
        scrollable_frame.grid_columnconfigure(1, minsize = 200)  # Column for "Name"
        scrollable_frame.grid_columnconfigure(2, minsize = 100)  # Column for "Gender"
        scrollable_frame.grid_columnconfigure(3, minsize = 150)  # Column for "Date"
        scrollable_frame.grid_columnconfigure(4, minsize = 100)  # Column for "Time"
        scrollable_frame.grid_columnconfigure(5, minsize = 150)  # Column for "Status"

        def update_scrollable_frame(attendance_data):
            # Clear existing rows
            for widget in scrollable_frame.winfo_children():
                widget.grid_forget()
            
            # Add headers
            headers = ["No", "Name", "Gender", "Date", "Time", "Attendant Status"]
            for col_index, header in enumerate(headers):
                ctk.CTkLabel(
                    scrollable_frame,
                    text = header,
                    font = ("Arial", 14, "bold"),
                    fg_color = "#4f4f4f",
                    text_color = "white",
                    corner_radius = 5
                ).grid(row = 0, column = col_index, padx = 5, pady = 5, sticky = "ew")

            # Add data rows with alternating row colors
            for row_index, record in enumerate(attendance_data, start = 1):
                row_color = "#2c2c2c" if row_index % 2 == 0 else "#1e1e1e"
                for col_index, field in enumerate(record):
                    ctk.CTkLabel(
                        scrollable_frame,
                        text = str(field),
                        font = ("Arial", 12),
                        fg_color = row_color,
                        text_color = "white",
                        corner_radius = 5
                    ).grid(row = row_index, column = col_index, padx = 5, pady = 5, sticky = "ew")
                
        # Initially populate with all attendance data
        update_scrollable_frame(get_all_attendance())
        
        # Add a back button
        ctk.CTkButton(
            customer_window,
            text = "Back",
            font = ("Arial", 16, "bold"),
            corner_radius = 20,
            width = 180,
            height = 60,
            fg_color = "#4C9EFF",
            hover_color = "#0066CC",
            text_color = "white", 
            border_width = 2,
            border_color = "#003366", 
            command = lambda: self.close_toplevel(customer_window)  
        ).pack(pady = 10, padx = 25, anchor = "e")
        

        
    def close_toplevel(self, customer_window):
        customer_window.destroy()
        self.app.deiconify()

if __name__ == "__main__":
    initialize()
    face_recognition_app = FaceRecognitionApp()
    face_recognition_app.run()