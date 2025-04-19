import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageTk
from tkinter import messagebox  
import login_screen  
import admin_login
from db_config import generate_food_quote

def open_login():
    """
    DESC:
        Closes the current homepage window and opens the customer login screen.

    :param: None
    :return: None
    """
    app.destroy()
    login_screen.show_login_screen()  # Closing the homepage window and call function to show login screen

quote = generate_food_quote()

def open_admin_login():
    """
    DESC:
        Closes the current homepage window and opens the Admin login screen.

    :param: None
    :return: None
    """
    app.destroy()
    admin_login.show_admin_login_screen() 

def show_details():
    """
    DESC:
        Displays an informational message box about the application, including developer details and application purpose.

    :param: None
    :return: None
    """

    message = (
        "Cook Mate - Recipe Finder\n\n"
        "Developed by:\n"
        "Amith Gundluri \n"
        "Venkat Phanindra Pasunooru\n"
        "Shivani Polagouni\n"
        "Srija Vadla\n"
        "Saichandu Anumula\n\n"
        "About Us:\n"
        "Cook Mate is designed to reduce food waste, simplify\n"
        "meal planning, and promote home cooking."
    )
    messagebox.showinfo("About Us", message)

def show_homepage():
    """
    DESC:
        Initializes and displays the main homepage window of the Cook Mate application. The homepage includes
        a logo, background image, navigation buttons (Explore Cooking, About Us, Admin Login), and frames
        for organizing content layout.

    :param: None
    :return: None
    
    """
    global app
    app = ctk.CTk()
    app.geometry("1024x600")
    app.title("Cook Mate - Recipe Finder")

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # Left Frame for Logo and Button
    left_frame = ctk.CTkFrame(app, width=455, height=1000, corner_radius=0, fg_color="white")
    left_frame.grid(row=0, column=0, sticky="nsew")

    # Right Frame for Background Image
    right_frame = ctk.CTkFrame(app, width=500, height=600, corner_radius=15, border_width=5, border_color="black")
    right_frame.grid(row=0, column=1, sticky="nsew")

    # Adjust row and column weights
    app.grid_columnconfigure(0, weight=65)
    app.grid_columnconfigure(1, weight=35)
    app.grid_rowconfigure(0, weight=1)

    # Adding the Logo to the Left Frame
    logo_image = Image.open("Assets/logo.png") 
    logo_photo = CTkImage(light_image=logo_image, size=(500, 500))  # Use CTkImage
    logo_label = ctk.CTkLabel(left_frame, image=logo_photo, text="")
    logo_label.place(relx=0.5, rely=0.3, anchor="center")

    # Explore Cooking Button that navigates to the login scree
    explore_button = ctk.CTkButton(left_frame, text="Explore Cooking", width=25, height=30,
                                font=("Lucida Handwriting", 12,'bold'),
                                corner_radius=30,
                                border_width=1,
                                border_color="#ffffff",
                                fg_color="#003366",
                                hover_color="#808080",
                                text_color="white",
                                command=open_login)  # Link to open_login function
    explore_button.place(relx=0.5, rely=0.60, anchor="center")

    # Adding Background Image to the Right Frame
    bg_image = Image.open("Assets/homepage.jpg")  
    bg_photo = CTkImage(light_image=bg_image, size=(750, 985))  # Use CTkImage
    bg_label = ctk.CTkLabel(right_frame, image=bg_photo, text="", corner_radius=15)
    bg_label.place(relx=0.5, rely=0.5, anchor="center")

    # About Us Button with Icon in Bottom Left Corner
    icon_image = Image.open("Assets/about.png") 
    icon_photo = CTkImage(dark_image=icon_image, size=(20, 20))  # Use CTkImage
    about_us_button = ctk.CTkButton(
        left_frame,
        text="About Gourmet Hub",
        width=30,
        height=30,
        font=("Angelina", 10, "bold"),
        corner_radius=30,
        fg_color="white",
        hover_color="#808080",
        text_color="#003366",
        image=icon_photo,  # Use CTkImage
        compound="left",  # Position the icon to the left of the text
        command=show_details,
    )
    about_us_button.place(relx=0.05, rely=0.80, anchor="sw")

    # Adding Admin Login Button next to the About Us Button
    admin_icon_image = Image.open("Assets/admin.png") 
    admin_icon_image = admin_icon_image.resize((20, 20), Image.Resampling.LANCZOS)
    admin_icon_photo = ImageTk.PhotoImage(admin_icon_image)

    admin_login_button = ctk.CTkButton(left_frame, text="Admin", width=30, height=30,
                                    font=("Montserrat", 14),
                                    corner_radius=40,
                                    fg_color="#003366",
                                    hover_color="#CCDAF5",
                                    text_color="white",
                                    compound="left",  
                                    command= open_admin_login)  
    admin_login_button.place(relx=0.7, rely=0.80, anchor="sw")  

    title_label = ctk.CTkLabel(left_frame, text=quote,
                               font=("Papyrus", 14, "bold"), text_color="#5b3222", justify="center",wraplength=400,corner_radius=40)
    title_label.place(relx=0.5, rely=0.90, anchor="center")


    # Run the homepage app
    app.mainloop()

if __name__ == "__main__":
    show_homepage()
