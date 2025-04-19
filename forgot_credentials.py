import customtkinter as ctk
import random
from tkinter import messagebox
from PIL import Image, ImageTk
import db_config
import re
import login_screen  # Import login screen for navigation


def show_forgot_credentials_screen():
    """
    Display the forgot credentials screen of the application.

    This function creates and configures the forgot credentials window, including all UI elements
    such as input fields, buttons, and images. It also sets up the necessary event
    handlers for user interactions.

    The forgot credentials screen allows users to:
    - Retrieve their username by providing name, email, and phone number
    - Reset their password by providing username and a new password
    - Return to the login screen

    No parameters or return value.
    """
    def validate_phone_number(phone):
        """
    Validate the format of a phone number.

    Args:
    phone (str): The phone number to validate.

    Returns:
    bool: True if the phone number is valid (10 digits), False otherwise.
    """
        return len(phone) == 10 and phone.isdigit()

    def validate_email(email):
        """
    Validate the format of an email address.

    Args:
    email (str): The email address to validate.

    Returns:
    bool: True if the email address is valid, False otherwise.
    """
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None
    
    def validate_password(password):
        """
    Validate the strength of a password.

    The password must:
    - Be at least 8 characters long
    - Contain at least one uppercase letter
    - Contain at least one digit
    - Contain at least one special character from !@#$%^&*()

    Args:
    password (str): The password to validate.

    Returns:
    bool: True if the password meets all criteria, False otherwise.
    """
        if (len(password) >= 8 and
            any(char.isupper() for char in password) and
            any(char.isdigit() for char in password) and
            any(char in "!@#$%^&*()" for char in password)):
            return True
        return False

    def retrieve_username():
        """
    Attempt to retrieve the user's username based on provided information.

    This function collects the name, email, and phone number entered by the user,
    validates the input, queries the database to find a matching user, and displays
    the username if found.

    If successful:
    - Displays the retrieved username in a message box
    - Returns the username

    If unsuccessful:
    - Displays an error message

    Returns:
    str or None: The retrieved username if found, None otherwise.
    """
        name = name_entry.get()
        email = email_entry.get()
        phone_number = phone_entry.get()
        if not validate_phone_number(phone_number) or not validate_email(email):
            messagebox.showwarning("Validation Error", "Please check your email and phone number format.")
            return
        query = "SELECT username FROM Users WHERE name = %s AND email = %s AND phone_number = %s"
        params = (name, email, phone_number)
        connection = db_config.create_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        db_config.close_connection(connection)
        if result:
            messagebox.showinfo("Username Retrieved", f"Your username is: {result[0]}")
            return result[0]
        else:
            messagebox.showerror("Error", "No matching user found. Please check your details.")

    def reset_password():
        """
        Attempt to reset the user's password.

        This function collects the username and new password entered by the user,
        validates the input, and updates the password in the database if the username exists.

        The password is stored as plain text in the database. Note: This is not recommended
        for production environments due to security concerns.

        If successful:
        - Updates the password in the database
        - Displays a success message

        If unsuccessful:
        - Displays an error message

        No return value.
        """
        username = username_entry.get()
        new_password = password_entry.get()
        if not username:
            messagebox.showerror("Error", "Please enter your username.")
            return
        if not validate_password(new_password):
            messagebox.showwarning("Password Requirements",
                                "Password must be at least 8 characters long, "
                                "contain one uppercase letter, one number, and one special character.")
            return
        query = "UPDATE Users SET password = %s WHERE username = %s"
        params = (new_password, username)
        try:
            db_config.execute_query(query, params)
            messagebox.showinfo("Success", "Password reset successfully!")
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    forgot_app = ctk.CTk()
    forgot_app.geometry("1000x600")
    forgot_app.title("Forgot Username or Password")

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    left_frame = ctk.CTkFrame(forgot_app, width=600, height=600, corner_radius=0, fg_color="#ffffff")
    left_frame.grid(row=0, column=1, sticky="nsew")

    right_frame = ctk.CTkFrame(forgot_app, width=400, height=600, corner_radius=0, fg_color="#003366")
    right_frame.grid(row=0, column=0, sticky="nsew")

    logo_image = Image.open("Assets/logo.png")
    logo_image = logo_image.resize((500, 500), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = ctk.CTkLabel(left_frame, image=logo_photo, text="")
    logo_label.place(relx=0.5, rely=0.35, anchor="center")

    title_label = ctk.CTkLabel(left_frame, text="Retrieve your credentials\nor reset your password",
                               font=("Tempus Sans ITC", 18, "bold"), text_color="#004ba0", justify="center")
    title_label.place(relx=0.5, rely=0.87, anchor="center")

    name_entry = ctk.CTkEntry(right_frame, placeholder_text="Name", width=200)
    name_entry.place(relx=0.1, rely=0.2, anchor="w")

    email_entry = ctk.CTkEntry(right_frame, placeholder_text="Email", width=200)
    email_entry.place(relx=0.1, rely=0.3, anchor="w")
    
    phone_entry = ctk.CTkEntry(right_frame, placeholder_text="Phone Number", width=200)
    phone_entry.place(relx=0.1, rely=0.4, anchor="w")

    username_entry = ctk.CTkEntry(right_frame, placeholder_text="Username", width=200)
    username_entry.place(relx=0.1, rely=0.5, anchor="w")

    password_entry = ctk.CTkEntry(right_frame, placeholder_text="New Password", show="*", width=200)
    password_entry.place(relx=0.1, rely=0.6, anchor="w")

    retrieve_button = ctk.CTkButton(right_frame, text="Retrieve Username", command=retrieve_username)
    retrieve_button.place(relx=0.1, rely=0.7, anchor="w")

    reset_button = ctk.CTkButton(right_frame, text="Reset Password", command=reset_password)
    reset_button.place(relx=0.1, rely=0.8, anchor="w")

    back_to_login_button = ctk.CTkButton(right_frame, text="Back to Login", command=lambda: [forgot_app.destroy(), login_screen.show_login_screen()])
    back_to_login_button.place(relx=0.1, rely=0.9, anchor="w")
    
    forgot_app.mainloop()

if __name__ == "__main__":
    show_forgot_credentials_screen()
