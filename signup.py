import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import db_config  # Import the database connection file
import login_screen  # Import login screen for navigation
import re  # For email validation

"""
Signup Screen Functions

This module provides the functionality for the signup screen of the Cook Mate application. It allows new users to
register by providing their details. The module includes validation for inputs like phone number, email, and password,
and checks for existing usernames or emails in the database.

Functions:
- `show_signup_screen`: Displays the main signup screen.
  - `validate_password`: Ensures the password meets the complexity requirements.
  - `validate_phone_number`: Checks if the phone number is valid (10 digits).
  - `validate_email`: Validates the email format using regex.
  - `check_existing_user`: Checks if the username or email is already registered in the database.
  - `signup`: Registers the user in the database after validating all inputs.
  - `show_password_requirements`: Displays password requirements in an informational message box.
"""

# Function to show the sign-up screen
def show_signup_screen():
    """
    DESC:
        Displays the signup screen, allowing users to enter their details and create an account. Validates the input 
        fields and ensures no duplicate accounts are created.

    :param: None
    :return: None
    """
    # Function to validate the password
    def validate_password(password):
        """
        DESC:
            Validates if the password meets the requirements: at least 8 characters, contains an uppercase letter, 
            a number, and a special character.

        :param password: str, The password to validate.
        :return: bool, True if valid, False otherwise.
        """
        if (len(password) >= 8 and
            any(char.isupper() for char in password) and
            any(char.isdigit() for char in password) and
            any(char in "!@#$%^&*()" for char in password)):
            return True
        return False

    # Function to validate phone number length
    def validate_phone_number(phone):
        """
        DESC:
            Checks if the phone number is exactly 10 digits.

        :param phone: str, The phone number to validate.
        :return: bool, True if valid, False otherwise.
        """
        return len(phone) == 10 and phone.isdigit()

    # Function to validate email format
    def validate_email(email):
        """
        DESC:
            Validates the email format using a regex.

        :param email: str, The email address to validate.
        :return: bool, True if valid, False otherwise.
        """
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    # Function to check if username or email exists
    def check_existing_user(username, email):
        """
        DESC:
            Checks if the provided username or email already exists in the database.

        :param username: str, The username to check.
        :param email: str, The email address to check.
        :return: bool, True if the username or email exists, False otherwise.
        """
        query = "SELECT * FROM Users WHERE username = %s OR email = %s"
        params = (username, email)
        connection = db_config.create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        db_config.close_connection(connection)
        return result is not None

    # Function to register the user
    def signup():
        """
        DESC:
            Registers a new user in the database after validating all input fields.

        :param: None
        :return: None
        """
        name = name_entry.get()
        username = username_entry.get()
        phone_number = phone_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        dietary_preference = dietary_pref_dropdown.get()

        # Validate phone number
        if not validate_phone_number(phone_number):
            messagebox.showwarning("Invalid Phone Number", "Phone number must be 10 digits long.")
            return

        # Validate email format
        if not validate_email(email):
            messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
            return

        # Validate password
        if not validate_password(password):
            messagebox.showwarning("Password Requirements",
                                   "Password must be at least 8 characters long, "
                                   "contain one uppercase letter, one number, and one special character.")
            return

        # Check if username or email already exists
        if check_existing_user(username, email):
            messagebox.showerror("Error", "Username or email already exists. Please try another.")
            return

        role = "user"  # Default for regular user

        # Insert new user into the database
        query = """INSERT INTO Users 
                   (name, username, password, phone_number, email, dietary_preference, role) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        params = (name, username, password, phone_number, email, dietary_preference, role)

        try:
            db_config.execute_query(query, params)
            messagebox.showinfo("Sign Up Successful", "Account created successfully! Redirecting to login page.")
            signup_app.destroy()
            login_screen.show_login_screen()  # Redirect to login page
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_password_requirements():
        """
        DESC:
            Displays a message box containing the password requirements.

        :param: None
        :return: None
        """
        messagebox.showinfo("Password Requirements",
                            "Your password must be at least 8 characters long, contain one uppercase letter, "
                            "one number, and one special character.")

    # Initialize the sign-up screen
    signup_app = ctk.CTk()
    signup_app.geometry("1000x600")
    signup_app.title("Signup Page")

    # Set light theme for blue and white colors
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # Left Frame for Logo and Text
    left_frame = ctk.CTkFrame(signup_app, width=400, height=600, corner_radius=0, fg_color="#003366")
    left_frame.grid(row=0, column=0, sticky="nsew")

    # Right Frame for Signup Form
    right_frame = ctk.CTkFrame(signup_app, width=600, height=600, corner_radius=0, fg_color="white")
    right_frame.grid(row=0, column=1, sticky="nsew")

    logo_image = Image.open("Assets/logo.png")  
    logo_image = logo_image.resize((670, 670), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = ctk.CTkLabel(left_frame, image=logo_photo, text="")
    logo_label.place(relx=0.5, rely=0.35, anchor="center")  # Position at the top

    quote = db_config.generate_food_quote()

    title_label = ctk.CTkLabel(left_frame, text=quote,
                               font=("Tempus Sans ITC",18, "bold"), text_color="white", justify="center",wraplength=300)
    title_label.place(relx=0.5, rely=0.87, anchor="center")

    # Signup Form
    form_title = ctk.CTkLabel(right_frame, text="Register User", font=("Helvetica", 22, "bold"), text_color="#003366")
    form_title.place(relx=0.1, rely=0.1, anchor="w")

    # Name Entry
    name_entry = ctk.CTkEntry(right_frame, placeholder_text="Name", width=200)
    name_entry.place(relx=0.1, rely=0.2, anchor="w")

    # Username Entry
    username_entry = ctk.CTkEntry(right_frame, placeholder_text="Username", width=200)
    username_entry.place(relx=0.55, rely=0.2, anchor="w")

    # Phone Number Entry
    phone_entry = ctk.CTkEntry(right_frame, placeholder_text="Phone Number", width=200)
    phone_entry.place(relx=0.1, rely=0.3, anchor="w")

    # Email Entry
    email_entry = ctk.CTkEntry(right_frame, placeholder_text="Email", width=200)
    email_entry.place(relx=0.55, rely=0.3, anchor="w")

    # Password Entry
    password_entry = ctk.CTkEntry(right_frame, placeholder_text="Password", width=200, show="*")
    password_entry.place(relx=0.1, rely=0.4, anchor="w")

    password_req_button = ctk.CTkButton(right_frame, text="Password Requirements", width=200, height=30,
                                        fg_color="gray", text_color="white", command=show_password_requirements)
    password_req_button.place(relx=0.55, rely=0.4, anchor="w")

    # Create Account Button
    create_account_button = ctk.CTkButton(right_frame, text="Create Account", width=400, height=40,
                                          fg_color="#004ba0", text_color="white", command=signup)
    create_account_button.place(relx=0.1, rely=0.6, anchor="w")

    # Login Link Button
    login_link = ctk.CTkButton(right_frame, text="Already have an account? Log in", font=("Helvetica", 12),
                               fg_color="#FFFFFF", text_color="#000000", command=lambda: [signup_app.destroy(), login_screen.show_login_screen()])
    login_link.place(relx=0.1, rely=0.7, anchor="w")

    # Dropdown for Dietary Preferences
    dietary_options = ["Vegetarian", "Non-Vegetarian", "Vegan", "Not Specific"]
    dietary_pref_dropdown = ctk.CTkOptionMenu(right_frame, values=dietary_options, width=200)
    dietary_pref_dropdown.set("Not Specific")  # Default value
    dietary_pref_dropdown.place(relx=0.55, rely=0.5, anchor="w")

    # Run the signup screen
    signup_app.mainloop()


if __name__ == "__main__":
     show_signup_screen()