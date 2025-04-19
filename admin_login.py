import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from customtkinter import CTkImage
import db_config
import admin_dashboard


def show_admin_login_screen():
    """
    DESC:
        Displays the admin login screen for the Cook Mate application. Provides input fields for username and 
        password, along with the functionality to toggle password visibility, validate admin credentials, 
        and navigate to other screens such as the signup screen or the homepage. The screen layout includes 
        a logo, a login form, and a background image.

    :param: None
    :return: None
    """
    def login():
        """
        Validates the username and password entered by the user. Checks against hardcoded admin credentials 
        or the database. Displays appropriate messages for login success or failure and redirects 
        to the admin dashboard if successful.

        :param: None
        :return: None
        """
        username = email_entry.get()
        password = password_entry.get()

        # Hardcoded admin credentials
        if username == "Admin" or username == 'admin' and password == "Admin@123":
            messagebox.showinfo("Login Success", "Welcome, Admin!")
            login_app.destroy()
            import admin_dashboard
            admin_dashboard.show_admin_dashboard({username})
            return

        query = "SELECT user_id, username, role FROM Users WHERE username = %s AND password = %s"
        params = (username, password)

        connection = db_config.create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchone()

        if result:
            user_id = result["user_id"]
            user_name = result["username"]
            role = result["role"]

            if role == 'admin':
                messagebox.showinfo("Login Success", f"Welcome, Admin {user_name}!")
                login_app.destroy()
                import admin_dashboard
                admin_dashboard.show_admin_dashboard(user_name)
            else:
                messagebox.showinfo("Login Success", f"Welcome, {user_name}!")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

        cursor.close()
        db_config.close_connection(connection)

    def toggle_password():
        """
        Toggles the visibility of the password field between obscured ('*') and visible text.

        :param: None
        :return: None
        """
        if password_entry.cget("show") == "*":
            password_entry.configure(show="")
        else:
            password_entry.configure(show="*")

    def open_signup_screen():
        """
        Navigates to the signup screen by closing the current login screen.

        :param: None
        :return: None
        """
        login_app.destroy()
        import signup

        signup.show_signup_screen()

    def load_image_safe(path, size):
        """
        Safely loads an image from the given path and resizes it to the specified size. Displays a warning if 
        the image is not found and substitutes a placeholder image.

        :param path: str, Path to the image file.
        :param size: tuple, Dimensions to resize the image.
        :return: PhotoImage object representing the loaded image.
        """
        try:
            image = Image.open(path)
            return ImageTk.PhotoImage(image.resize(size, Image.Resampling.LANCZOS))
        except FileNotFoundError:
            messagebox.showwarning("Asset Missing", f"Image not found: {path}")
            placeholder = Image.new("RGB", size, "gray")
            return ImageTk.PhotoImage(placeholder)
        
    def on_back_callback():
        """
        Navigates back to the homepage by closing the current login screen.

        :param: None
        :return: None
        """
        login_app.destroy()
        import app
        app.show_homepage()

    # Initialize the login application
    login_app = ctk.CTk()
    login_app.geometry("1000x600")
    login_app.title("Admin Login Screen")

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # Image references to prevent garbage collection
    images = {}

    # Left Frame
    left_frame = ctk.CTkFrame(login_app, width=250, height=600, corner_radius=50, fg_color="#ffffff")
    left_frame.grid(row=0, column=0, sticky="nsew")

    # Right Frame
    right_frame = ctk.CTkFrame(login_app, width=350, height=600, corner_radius=60,fg_color="#000000")
    right_frame.grid(row=0, column=1, sticky="nsew")

    login_app.grid_columnconfigure(0, weight=65)
    login_app.grid_columnconfigure(1, weight=35)
    login_app.grid_rowconfigure(0, weight=1)

    # Load and store images
    # logo_image = Image.open("Assets/logo.png")
    # images["logo_photo1"] = CTkImage(light_image=logo_image, size=(200, 200))
    # logo_label = ctk.CTkLabel(left_frame, image=images["logo_photo1"], text="")
    # logo_label.place(relx=0.5, rely=0.20, anchor="center")

    logo_photo1 = load_image_safe("Assets/logo.png", (390, 395))
    logo_label = ctk.CTkLabel(left_frame, image=logo_photo1, text="")
    logo_label.image = logo_photo1  # Prevent garbage collection
    logo_label.place(relx=0.5, rely=0.20, anchor="center")

    email_label = ctk.CTkLabel(left_frame, text="Username", font=("Helvetica", 14), text_color="Black")
    email_label.place(relx=0.25, rely=0.40, anchor="w")
    email_entry = ctk.CTkEntry(left_frame, placeholder_text="Enter your Username", width=250)
    email_entry.place(relx=0.25, rely=0.42)

    password_label = ctk.CTkLabel(left_frame, text="Password", font=("Helvetica", 14), text_color="Black")
    password_label.place(relx=0.25, rely=0.50, anchor="w")
    password_entry = ctk.CTkEntry(left_frame, placeholder_text="Enter your password", show="*", width=250)
    password_entry.place(relx=0.25, rely=0.52)

    # Load and store eye icon image
    eye_icon = load_image_safe("Assets/eye.png", (20, 20))
    # images["eye_icon_photo"] = CTkImage(light_image=eye_icon, size=(20, 20))
    toggle_button = ctk.CTkButton(
        left_frame,
        image=eye_icon,
        text="",
        width=30,
        height=30,
        fg_color="white",
        hover_color="#d9d9d9",
        command=toggle_password,
    )
    toggle_button.place(relx=0.75, rely=0.54, anchor="w")

    # Login Button
    # Log In Button
    login_button = ctk.CTkButton(
        left_frame,
        text="Log In",
        width=150,
        height=30,
        corner_radius=40,
        fg_color="#003366",
        text_color="#ffffff",
        command=login,
    )
    login_button.place(relx=0.35, rely=0.70, anchor="center")

    # Back Button
    back_button = ctk.CTkButton(
        left_frame,
        text="Back",
        width=150,
        height=30,
        fg_color="red",
        corner_radius=40,
        text_color="#ffffff",
        command=on_back_callback,
    )
    back_button.place(relx=0.65, rely=0.70, anchor="center")  # Positioned next to the Login button


    # Load and store background image
    bg_image = Image.open("Assets/admin_screen.jpg")
    images["bg_photo"] = CTkImage(light_image=bg_image, size=(350, 600))
    bg_label = ctk.CTkLabel(right_frame, image=images["bg_photo"], text="")
    bg_label.place(relx=0, rely=0, relwidth=1, relheight=1, anchor="nw")
    login_app.mainloop()


if __name__ == "__main__":
    show_admin_login_screen()
