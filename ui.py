import customtkinter as ctk

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Animation Example")
        
        # Initial size of the frame
        self.right_frame = ctk.CTkFrame(self, fg_color="#0c0c0c", corner_radius=15)
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        
        # Start the animation
        self.animate_frame(100, 300, 100, 200, 0)  # Start animation from (100, 100) to (300, 200)
    
    def animate_frame(self, start_width, end_width, start_height, end_height, step):
        if step <= 50:  # This will animate for 50 steps
            # Calculate the new width and height
            width = start_width + (end_width - start_width) * (step / 50)
            height = start_height + (end_height - start_height) * (step / 50)

            # Update the size of the frame using 'configure' instead of 'config'
            self.right_frame.configure(width=width, height=height)

            # Schedule the next step of the animation
            self.after(50, self.animate_frame, start_width, end_width, start_height, end_height, step + 1)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
