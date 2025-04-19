import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import db_config  # Import the database connection file
import signup  # Import signup screen for navigation
import forgot_credentials  # Import forgot credentials screen for navigation
import user_home  # Import the user home page for navigation after login

def show_login_screen():
    """
    Display the main login screen of the application.

    This function creates and configures the login window, including all UI elements
    such as input fields, buttons, and images. It also sets up the necessary event
    handlers for user interactions.

    The login screen allows users to:
    - Enter their username and password
    - Toggle password visibility
    - Attempt to log in
    - Navigate to the signup screen
    - Navigate to the forgot credentials screen
    - Return to the homepage

    No parameters or return value.
    """
    def login():
        """
    Attempt to authenticate the user with the provided credentials.

    This function retrieves the entered username and password, queries the database
    to verify the credentials, and takes appropriate action based on the result.

    If authentication is successful:
    - Displays a welcome message
    - Closes the login window
    - Opens the user's home page

    If authentication fails:
    - Displays an error message

    No parameters or return value.
    """
        username = email_entry.get()
        password = password_entry.get()
        query = "SELECT user_id, username FROM Users WHERE username = %s AND password = %s"
        params = (username, password)
        connection = db_config.create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result:
            user_id = result["user_id"]
            user_name = result["username"]
            messagebox.showinfo("Login Success", f"Welcome, {user_name}!")
            login_app.destroy()
            user_home.show_user_home(user_id, user_name)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
        cursor.close()
        db_config.close_connection(connection)

    def onClick_back_button():
        """
        Handle the event when the back button is clicked.

        This function closes the current login window and returns the user to the homepage.

        No parameters or return value.
        """
        login_app.destroy()
        import app
        app.show_homepage()

    def toggle_password():
        """
    Toggle the visibility of the password in the password entry field.

    This function switches the password entry between showing asterisks and 
    showing the actual characters.

    No parameters or return value.
    """
        if password_entry.cget("show") == "*":
            password_entry.configure(show="")
        else:
            password_entry.configure(show="*")

    def open_signup_screen():
        """
    Navigate to the signup screen.

    This function closes the current login window and opens the signup screen.

    No parameters or return value.
    """
        login_app.destroy()
        signup.show_signup_screen()

    def open_forgot_credentials_screen():
        """
    Navigate to the forgot credentials screen.

    This function closes the current login window and opens the forgot credentials screen.

    No parameters or return value.
    """
        login_app.destroy()
        forgot_credentials.show_forgot_credentials_screen()

    login_app = ctk.CTk()
    login_app.geometry("1000x600")
    login_app.title("Login Screen")

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    left_frame = ctk.CTkFrame(login_app, width=250, height=600, corner_radius=0, fg_color="#FFFFFF")
    left_frame.grid(row=0, column=0, sticky="nsew")

    right_frame = ctk.CTkFrame(login_app, width=350, height=600, corner_radius=0)
    right_frame.grid(row=0, column=1, sticky="nsew")

    login_app.grid_columnconfigure(0, weight=65)
    login_app.grid_columnconfigure(1, weight=35)
    login_app.grid_rowconfigure(0, weight=1)

    logo_image = Image.open("Assets/logo.png")
    logo_image = logo_image.resize((390, 395), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = ctk.CTkLabel(left_frame, image=logo_photo, text="")
    logo_label.place(relx=0.5, rely=0.20, anchor="center")

    email_label = ctk.CTkLabel(left_frame, text="Username", font=("Helvetica", 14), text_color="Black")
    email_label.place(relx=0.25, rely=0.40, anchor="w")
    email_entry = ctk.CTkEntry(left_frame, placeholder_text="Enter your Username", width=250)
    email_entry.place(relx=0.25, rely=0.42)

    password_label = ctk.CTkLabel(left_frame, text="Password", font=("Helvetica", 14), text_color="Black")
    password_label.place(relx=0.25, rely=0.50, anchor="w")

    password_entry = ctk.CTkEntry(left_frame, placeholder_text="Enter your password", show="*", width=250)
    password_entry.place(relx=0.25, rely=0.52)

    eye_icon = Image.open("Assets/eye.png")
    eye_icon = eye_icon.resize((20, 20), Image.Resampling.LANCZOS)
    eye_icon_photo = ImageTk.PhotoImage(eye_icon)

    toggle_button = ctk.CTkButton(left_frame, image=eye_icon_photo, text="", width=30, height=30, fg_color="white", hover_color="#d9d9d9", command=toggle_password)
    toggle_button.place(relx=0.75, rely=0.54, anchor="w")

    login_button = ctk.CTkButton(left_frame, text="Log In", width=150, height=30, fg_color="#003366", text_color="#ffffff", command=login)
    login_button.place(relx=0.25, rely=0.60)

    back_button = ctk.CTkButton(left_frame, text="Back", width=150, height=30, fg_color="#003366", text_color="#ffffff", command=onClick_back_button)
    back_button.place(relx=0.55, rely=0.60)

    signup_button = ctk.CTkButton(left_frame, text="New User SignUp?", font=("Helvetica", 12, "bold"), text_color="blue", fg_color="#ffffff", command=open_signup_screen)
    signup_button.place(relx=0.25, rely=0.73, anchor="w")

    forgot_button = ctk.CTkButton(left_frame, text="Forgot Username/Password?", font=("Helvetica", 12, "bold"), text_color="Red", fg_color="#ffffff", command=open_forgot_credentials_screen)
    forgot_button.place(relx=0.25, rely=0.78, anchor="w")

    bg_image = Image.open("Assets/login.jpg")
    bg_image = bg_image.resize((950, 1000), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = ctk.CTkLabel(right_frame, image=bg_photo, text="")
    bg_label.place(relx=0, rely=0, relwidth=1, relheight=1, anchor="nw")

    login_app.mainloop()

if __name__ == "__main__":
    show_login_screen()
