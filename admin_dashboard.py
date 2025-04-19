import os
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox, Canvas, Scrollbar,Toplevel
from tkinter import ttk
from PIL import Image, ImageTk
from PIL import ImageGrab
#import tempfile
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import admin_utils

"""
Admin Dashboard Functions

This module provides the functionality for the Admin Dashboard of Cook Mate. It includes features like user and recipe 
management, generating reports, visualizing insights, and more. Below is a summary of the main functions and their 
descriptions:

- `logout_to_home`: Logs out of the admin dashboard and redirects to the homepage.
- `show_admin_dashboard`: Displays the main admin dashboard with navigation options and user-specific content.
- `manage_recipes`: Displays all recipes and provides options to edit or delete them.
- `edit_recipe`: Allows editing details of a specific recipe.
- `delete_recipe`: Deletes a specific recipe from the database after confirmation.
- `manage_users`: Displays all users and provides options to edit their roles or delete them.
- `edit_user_role`: Allows editing the role of a specific user.
- `delete_user`: Deletes a user from the database after confirmation.
- `show_insights`: Displays insights and analytics using visualizations such as charts and tables.
- `generate_reports`: Provides functionality to generate and download analytics reports.
- `add_recipe`: Allows adding a new recipe with multiple fields including ingredients, procedure, and dietary conditions.

Function Summaries
"""

def show_home_content(content_frame, username):

    print("show_home_content",username);
    """
    DESC:
        Displays the home content with all available navigation buttons and a logo.

    :param content_frame: CTkFrame, the content area frame for displaying content.
    :param username: str, The username of the logged-in admin.
    :return: None
    """
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Display the Cook Mate logo
    icon_path = "Assets/logo - Copy.png"  # Adjust to your logo's path
    cookmate_icon = ctk.CTkImage(
        light_image=Image.open(icon_path),
        size=(300, 300)  # Adjust the size of the icon as needed
    )
    logo_label = ctk.CTkLabel(content_frame, image=cookmate_icon, text="", compound="top")
    logo_label.pack(pady=20)

    # Define buttons with icons
    buttons = [
        ("Assets/addrecipie.png", "Add Recipe", lambda: add_recipe(content_frame)),
        ("Assets/manage recipie.png", "Manage Recipes", lambda: manage_recipes(content_frame)),
        ("Assets/manage.png", "Manage Users", lambda: manage_users(content_frame)),
        ("Assets/analytics.png", "Insights & Analytics", lambda: show_insights(content_frame,username)),
        #("Assets/Report.png", "Generate Reports", lambda: generate_reports(content_frame, username)),
    ]

    for icon_path, text, command in buttons:
        # Create an icon for the button
        icon_image = ctk.CTkImage(
            light_image=Image.open(icon_path),
            size=(20, 20)  # Adjust size as needed
        )

        # Create button with icon and text
        ctk.CTkButton(
            content_frame,
            image=icon_image,
            text=text,
            fg_color="#003366",
            compound="left",  # Icon placed to the left of text
            font=("Arial", 14),
            width=200,
            height=50,
            corner_radius=90,
            command=command
        ).pack(pady=10)


def logout_to_home():
    """
    DESC:
        Logs out the admin user and navigates back to the homepage.

    :param: None
    :return: None
    """
    admin_root.destroy()
    import app
    app.show_homepage()
    return

def show_user_home_content(content_frame,username):

    """
    DESC:
        Displays a personalized welcome message for the user in the content frame.

    :param content_frame: CTkFrame, the content area frame for displaying content.
    :param username: str, The username of the logged-in user.
    :return: None
    """
    #     widget.destroy(),
    
    # Display Welcome message
    welcome_label = ctk.CTkLabel(content_frame, text=f"Welcome to CookMate, {username} ",
                                 font=("Arial", 24), text_color='black')
    welcome_label.pack(pady=20)
    icon_path = "Assets/logo - copy.png"  # Path to your Cook Mate icon
    cookmate_icon = ctk.CTkImage(
    light_image=Image.open(icon_path),
    size=(150, 100) 
    )
# Admin Dashboard
def show_admin_dashboard(username=''):
    """
    DESC:
        Displays the admin dashboard with a sidebar containing navigation buttons (e.g., Manage Recipes, Insights & Analytics).
        The main content area shows user-specific content and updates based on the selected action.

    :param username: str, Optional, the username of the logged-in admin.
    :return: None
    """
    global admin_root
    admin_root = ctk.CTk()
    admin_root.title("Admin Dashboard")
    admin_root.geometry("1200x700")
   
    # Grid Layout
    admin_root.rowconfigure(0, weight=1)
    admin_root.columnconfigure(1, weight=1)

    # Sidebar
    sidebar_frame = ctk.CTkFrame(admin_root, width=200, fg_color="#004aad", corner_radius=0)
    sidebar_frame.grid(row=0, column=0, sticky="ns")
    sidebar_frame.grid_propagate(False)
    
    # Add Active User Label
    # active_user_label = ctk.CTkLabel(
    #     sidebar_frame,
    #     text=f"Cook Mate:\n{username}",
    #     font=("Arial", 16, "bold"),
    #     text_color="white",
    #     justify="center"
    # )
    # active_user_label.pack(pady=20)

    # Add Active User Label with Icon
    active_user_label = ctk.CTkLabel(sidebar_frame,
    #image=cookmate_icon,  # Set the icon
    text=f"{username}",  # Display only the username
    font=("Arial", 16, "bold"),
    text_color="white",
    compound="top",  # Place the icon above the username
    justify="center"
    )
    active_user_label.pack(pady=20)


    # Content area
    content_frame = ctk.CTkFrame(admin_root, fg_color="white")
    content_frame.grid(row=0, column=1, sticky="nsew")
    show_home_content(content_frame, username)

    # Sidebar Buttons with Icons
    admin_buttons = [
        ("Assets/home.png", "Home", lambda: show_home_content(content_frame, username)),
        ("Assets/addrecipie.png", "Add Recipe", lambda: add_recipe(content_frame)),
        ("Assets/manage recipie.png", "Manage Recipes", lambda: manage_recipes(content_frame)),
        ("Assets/manage.png", "Manage Users", lambda: manage_users(content_frame)),
        ("Assets/analytics.png", "Insights & Analytics", lambda: show_insights(content_frame)),
        #("Assets/Report.png", "Generate Reports", lambda: generate_reports(content_frame, username)),
        ("Assets/logout.png", "Logout", lambda: logout_to_home())
    ]

    for icon_path, tooltip_text, command in admin_buttons:
        icon_image = ctk.CTkImage(
            light_image=Image.open(icon_path),
            size=(30, 30)  # Adjust size as needed
        )

        # Create button with icon
        button = ctk.CTkButton(
            sidebar_frame,
            image=icon_image,
            text="",  # No text for buttons
            compound="left",  # Icon-only layout
            command=command,
            height=40,
            width=100,
            corner_radius=10,
        )
        button.pack(pady=10, padx=10)

        # Tooltip for each button
        def on_enter(event, tooltip_text=tooltip_text):
            button_x = button.winfo_rootx()
            button_y = button.winfo_rooty()
            button_width = button.winfo_width()

            tooltip = ctk.CTkLabel(
                admin_root,
                text=tooltip_text,
                font=("Arial", 14),
                fg_color="#003366",
                text_color="#ffffff",
                corner_radius=5
            )
            tooltip.place(x=event.x_root - admin_root.winfo_x() + 0, y=event.y_root - admin_root.winfo_y())
            event.widget.tooltip = tooltip

        def on_leave(event):
            event.widget.tooltip.destroy()

        button.bind("<Enter>", lambda e, text=tooltip_text: on_enter(e, text))
        button.bind("<Leave>", on_leave)

    admin_root.mainloop()


# Manage Recipes

def manage_recipes(content_frame):
    """
    DESC:
        Displays all recipes in a 4x4 grid layout, allowing the admin to edit or delete each recipe.
        Includes a search bar to filter recipes by name or ID.

    :param content_frame: CTkFrame, the content area frame where recipes will be displayed.
    :return: None
    """
    def load_recipes(search_query=""):
        """
        Filters and displays recipes based on the search query.
        :param search_query: str, the query to filter recipes by name or ID.
        """
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        filtered_recipes = [r for r in recipes if search_query.lower() in r['name'].lower() or str(r['recipe_id']).startswith(search_query)]
        if filtered_recipes:
            ctk.CTkLabel(scrollable_frame, text="Manage Recipes", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

            # Load Icon
            icon_image = Image.open("Assets/notes.png")  # Replace with the path to your icon file
            icon_image = icon_image.resize((50, 50), Image.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_image)

            for idx, recipe in enumerate(filtered_recipes):
                row = (idx // 9) + 1
                col = idx % 9

                # Recipe Frame
                recipe_frame = ctk.CTkFrame(scrollable_frame, fg_color="lightgray", corner_radius=5)
                recipe_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

                # Recipe Icon
                recipe_icon_label = ctk.CTkLabel(recipe_frame, image=icon_photo, text="", fg_color="lightgray")
                recipe_icon_label.image = icon_photo  # Keep a reference to avoid garbage collection
                recipe_icon_label.pack(pady=5)

                # Recipe Name
                recipe_label = ctk.CTkLabel(recipe_frame, text=recipe['name'], font=("Arial", 12, "bold"), wraplength=100)
                recipe_label.pack(pady=5)

                # Edit Button
                ctk.CTkButton(
                    recipe_frame, text="Edit", command=lambda r=recipe: edit_recipe(content_frame, r), width=80
                ).pack(pady=5)

                # Delete Button
                ctk.CTkButton(
                    recipe_frame,
                    text="Delete",
                    fg_color="red",
                    command=lambda r_id=recipe['recipe_id']: admin_utils.popup_authentication(
                        action="delete",
                        user_id=r_id,
                        content_frame=content_frame
                    ),
                    width=80
                ).pack(pady=5)
        else:
            ctk.CTkLabel(scrollable_frame, text="No recipes found.", font=("Arial", 14, "italic")).pack(pady=20)

    for widget in content_frame.winfo_children():
        widget.destroy()

    # Search Bar Frame
    search_frame = ctk.CTkFrame(content_frame, fg_color="white")
    search_frame.pack(fill="x", pady=10)

    ctk.CTkLabel(search_frame, text="Search Recipe:", font=("Arial", 14)).pack(side="left", padx=(10, 5))

    search_entry = ctk.CTkEntry(search_frame, font=("Arial", 12), width=300)
    search_entry.pack(side="left", padx=5)

    def on_search():
        search_query = search_entry.get()
        load_recipes(search_query)

    ctk.CTkButton(search_frame, text="Search", command=on_search).pack(side="left", padx=10)

    # Recipe List Canvas and Scrollbar
    canvas = Canvas(content_frame, bg="white")
    canvas.pack(side="left", fill="both", expand=True)

    vertical_scrollbar = Scrollbar(content_frame, orient="vertical", command=canvas.yview)
    vertical_scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=vertical_scrollbar.set)

    scrollable_frame = ctk.CTkFrame(canvas, fg_color="white")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Fetch recipes
    recipes = admin_utils.get_all_recipes()
    load_recipes()  # Load all recipes initially

    # Adjust Grid Weights
    for col in range(4):
        scrollable_frame.grid_columnconfigure(col, weight=1)


# Edit Recipe
def edit_recipe(content_frame, recipe):
    """
    Opens a new window to edit details of a specific recipe after admin authentication.
    """
    # Create the edit window
    edit_window = ctk.CTkToplevel()
    edit_window.title("Edit Recipe")
    edit_window.geometry("700x600")
    edit_window.resizable(False, False)
    edit_window.configure(fg_color="#f4f4f4")
    edit_window.transient(content_frame)
    edit_window.grab_set()
    edit_window.focus_set()

    # Header Title
    ctk.CTkLabel(
        edit_window, text="Edit Recipe Details", font=("Arial", 20, "bold"),
        fg_color="#3B82F6", corner_radius=8, text_color="white", height=40
    ).pack(fill="x", pady=10)

    # Form Frame
    form_frame = ctk.CTkFrame(edit_window, fg_color="white", corner_radius=10)
    form_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Fields
    fields = {
        "Name": recipe['name'],
        "Ingredients": recipe['ingredients'],
        "Dietary Condition": recipe['dietary_condition'],
        "Time Taken": recipe['time_taken'],
        "YouTube Link": recipe['youtube_link']
    }

    entries = {}
    for idx, (label, value) in enumerate(fields.items()):
        ctk.CTkLabel(form_frame, text=label, font=("Arial", 14), anchor="w").grid(
            row=idx, column=0, pady=10, padx=10, sticky="w"
        )
        entry = ctk.CTkEntry(form_frame, width=500, font=("Arial", 12))
        entry.insert(0, value)
        entry.grid(row=idx, column=1, pady=10, padx=10, sticky="w")
        entries[label] = entry

    # Procedure field
    ctk.CTkLabel(form_frame, text="Procedure", font=("Arial", 14), anchor="w").grid(
        row=len(fields), column=0, pady=10, padx=10, sticky="nw"
    )
    procedure_textbox = ctk.CTkTextbox(form_frame, width=500, height=150, font=("Arial", 12))
    procedure_textbox.insert("1.0", recipe['steps'])
    procedure_textbox.grid(row=len(fields), column=1, pady=10, padx=10, sticky="w")

    # Button frame
    button_frame = ctk.CTkFrame(edit_window, fg_color="#f4f4f4")
    button_frame.pack(pady=10)

    # Save Changes action
    def save_changes():
        """
        Save the updated recipe details after authenticating the admin.
        """
        if admin_utils.authenticate_admin():  # Call authentication function
            updated_values = {key: entry.get() for key, entry in entries.items()}
            updated_values['Procedure'] = procedure_textbox.get("1.0", "end").strip()
            updated_values['recipe_id'] = recipe['recipe_id']
            admin_utils.update_recipe(updated_values)  # Update the recipe in the database
            messagebox.showinfo("Success", "Recipe updated successfully!")
            edit_window.destroy()  # Close the edit window
            manage_recipes(content_frame)  # Refresh the recipe management view
        else:
            messagebox.showerror("Permission Denied", "Admin authentication failed. Cannot save changes.")

    # Cancel action
    def cancel_edit():
        edit_window.destroy()

    # Add buttons
    ctk.CTkButton(
        button_frame, text="Save Changes", command=save_changes,
        fg_color="#10B981", hover_color="#059669", font=("Arial", 14), corner_radius=8
    ).grid(row=0, column=0, padx=10, pady=10)
    
    ctk.CTkButton(
        button_frame, text="Cancel", command=cancel_edit,
        fg_color="#EF4444", hover_color="#DC2626", font=("Arial", 14), corner_radius=8
    ).grid(row=0, column=1, padx=10, pady=10)



# Delete Recipe
def delete_recipe(content_frame, recipe_id):
    """
    Deletes a specific recipe after admin authentication and confirmation.
    """
    if admin_utils.authenticate_admin():  # Call authentication function
        if messagebox.askyesno("Delete Recipe", "Are you sure?"):
            admin_utils.delete_recipe(recipe_id)  # Delete the recipe from the database
            manage_recipes(content_frame)  # Refresh the recipe management view
    else:
        messagebox.showerror("Permission Denied", "Admin authentication failed. Cannot delete recipe.")



def manage_users(content_frame):
    """
    DESC:
        Displays all users in a grid format with a search bar and options to edit roles or delete users.

    :param content_frame: CTkFrame, the content area frame where users will be displayed.
    :return: None
    """
    # Clear the existing content in the content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Create a canvas for scrolling
    canvas = Canvas(content_frame, bg="white")
    canvas.pack(side="left", fill="both", expand=True)

    # Add vertical scrollbar
    vertical_scrollbar = Scrollbar(content_frame, orient="vertical", command=canvas.yview)
    vertical_scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=vertical_scrollbar.set)

    # Create a frame inside the canvas
    scrollable_frame = ctk.CTkFrame(canvas, fg_color="white")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Search Bar
    search_frame = ctk.CTkFrame(scrollable_frame, fg_color="white")
    search_frame.grid(row=0, column=0, columnspan=4, pady=10, sticky="ew")  # Ensure it spans all columns

    # Add a search label and entry
    ctk.CTkLabel(search_frame, text="Search:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    search_var = ctk.StringVar()
    search_entry = ctk.CTkEntry(search_frame, textvariable=search_var, width=200)
    search_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    def perform_search():
        search_term = search_var.get().strip().lower()
        filtered_users = [
            user for user in admin_utils.get_all_users()
            if search_term in str(user['user_id']).lower() or search_term in user['name'].lower()
        ]
        display_users(scrollable_frame, filtered_users)

    # Add search and reset buttons
    search_button = ctk.CTkButton(
        search_frame,
        text="Search",
        command=perform_search,
        width=80
    )
    search_button.grid(row=0, column=2, padx=10, pady=5, sticky="w")

    reset_button = ctk.CTkButton(
        search_frame,
        text="Reset",
        command=lambda: display_users(scrollable_frame, admin_utils.get_all_users()),
        width=80
    )
    reset_button.grid(row=0, column=3, padx=10, pady=5, sticky="w")


    # Fetch users and display them
    try:
        users = admin_utils.get_all_users()
        display_users(scrollable_frame, users)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load users: {e}")


def display_users(frame, users):
    """
    DESC:
        Displays users in a grid format with options to edit roles or delete users.

    :param frame: CTkFrame, the frame where user information will be displayed.
    :param users: list, List of user dictionaries to display.
    :return: None
    """
    # Clear existing user widgets
    for widget in frame.winfo_children():
        if not isinstance(widget, ctk.CTkFrame):
            widget.destroy()

    if users:
        for idx, user in enumerate(users):
            row_idx = idx // 5 + 1  # Determine the row (4 items per row, starting from row 1)
            col_idx = idx % 5  # Determine the column

            # Create a user frame for styling
            user_frame = ctk.CTkFrame(frame, fg_color="#f0f0f0", corner_radius=10)  # Light gray background
            user_frame.grid(
                row=row_idx,
                column=col_idx,
                padx=10,  # Horizontal padding between columns
                pady=20,  # Vertical padding between rows (increased for row spacing)
                sticky="nsew"
            )

            # Configure grid column and row weights (optional, for better scaling)
            frame.grid_columnconfigure(col_idx, weight=1)
            frame.grid_rowconfigure(row_idx, weight=1)

            # User details
            icon_label = ctk.CTkLabel(user_frame, text="👤", font=("Arial", 24))
            icon_label.pack(pady=5)

            user_label = ctk.CTkLabel(
                user_frame,
                text=f"ID: {user['user_id']}\nName: {user['name']}",
                font=("Arial", 14),
                justify="center",
                text_color="black"
            )
            user_label.pack(pady=5)

            # Role dropdown
            role_var = ctk.StringVar(value=user['role'])
            role_dropdown = ctk.CTkOptionMenu(
                user_frame,
                variable=role_var,
                values=["user", "admin"]
            )
            role_dropdown.pack(pady=5)

            # Save Changes button
            save_button = ctk.CTkButton(
                user_frame,
                text="Save Changes",
                command=lambda u=user, role_var=role_var: save_user_role(frame, u, role_var.get()),
                width=100
            )
            save_button.pack(pady=5)

            # Delete button
            delete_button = ctk.CTkButton(
                user_frame,
                text="Delete",
                fg_color="red",
                command=lambda u_id=user['user_id']: delete_user(frame, u_id),
                width=100
            )
            delete_button.pack(pady=5)
    else:
        ctk.CTkLabel(frame, text="No users found.", font=("Arial", 14)).grid(row=1, column=0, columnspan=4, pady=20, sticky="center")



def save_user_role(content_frame, user, new_role):
    """
    Opens authentication popup before changing user role.

    :param content_frame: CTkFrame, The content area frame for refreshing the view post-update.
    :param user: dict, The user details.
    :param new_role: str, The new role to be updated.
    :return: None
    """
    if user['role'] == new_role:  # No changes
        messagebox.showinfo("No Change", "No changes were made.")
        return

    # Open authentication popup
    admin_utils.popup_authentication("change_role", user_id=user['user_id'], new_role=new_role, content_frame=content_frame)


# Update the delete_user function to use the popup
def delete_user(content_frame, user_id):
    """
    Opens authentication popup before deleting a user.

    :param content_frame: CTkFrame, The content area frame for refreshing the view post-deletion.
    :param user_id: int, The unique identifier of the user to delete.
    :return: None
    """
    # Open authentication popup
    admin_utils.popup_authentication("delete", user_id=user_id, content_frame=content_frame)


# Show Insights
def show_insights(content_frame, username = ''):

    print("show_insights",username);
    """
    DESC:
        Displays insights and analytics using visualizations such as bar charts, pie charts, and tables.

    :param content_frame: CTkFrame, the content area frame where insights will be displayed.
    :return: None
    """
    # Clear existing content in the frame
    for widget in content_frame.winfo_children():
        widget.destroy()
    username = username
    Analytics_button = ctk.CTkButton(
    content_frame,
    text="Download Report",
    command=lambda: admin_utils.generate_analytics_report(username)
    )

    Analytics_button.grid(row=3, column=1, columnspan=1, pady=20)

    # Fetch insights
    insights = admin_utils.get_insights()
    if not insights:
        messagebox.showerror("Error", "Failed to fetch insights")
        return

    # Display total users and recipes at the top
    header_frame = ctk.CTkFrame(content_frame, fg_color="white")
    header_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    ctk.CTkLabel(
        header_frame,
        text=f"Total Users: {insights['total_users']} | Total Recipes: {insights['total_recipes']}",
        font=("Arial", 18, "bold"),
    ).pack(pady=10)

    # Configure grid for multiple visualizations
    content_frame.rowconfigure([1, 2], weight=1)
    content_frame.columnconfigure([0, 1], weight=1)

    ### Visualization 1: Bar Chart - Number of Recipes vs. Dietary Conditions ###
    diet_chart_frame = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=10)
    diet_chart_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    fig1, ax1 = plt.subplots(figsize=(5, 3))
    ax1.bar(insights['dietary_conditions'], insights['counts'], color='skyblue')
    ax1.set_title("Number of Recipes by Dietary Conditions", fontsize=14)
    ax1.set_xlabel("Dietary Conditions", fontsize=12)
    ax1.set_ylabel("Number of Recipes", fontsize=12)
    fig1.tight_layout()

    chart1 = FigureCanvasTkAgg(fig1, master=diet_chart_frame)
    chart1.get_tk_widget().pack(fill="both", expand=True)

    ### Visualization 2: Pie Chart - Users vs. Dietary Preferences ###
    pie_chart_frame = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=10)
    pie_chart_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    fig2, ax2 = plt.subplots(figsize=(5, 3))
    ax2.pie(
        insights['user_diet_counts'],
        labels=insights['user_dietary_preferences'],
        autopct="%1.1f%%",
        startangle=140,
        colors=plt.cm.Paired.colors
    )
    ax2.set_title("Users by Dietary Preferences", fontsize=14)
    fig2.tight_layout()

    chart2 = FigureCanvasTkAgg(fig2, master=pie_chart_frame)
    chart2.get_tk_widget().pack(fill="both", expand=True)

    ### Visualization 3: Table - Users vs. Number of Recipes Added ###
    table_frame = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=10)
    table_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    # Create Treeview with professional styling
    style = ttk.Style()
    style.configure(
        "Treeview",
        font=("Arial", 12),
        rowheight=30,
        background="#f9f9f9",
        fieldbackground="#f9f9f9",
    )
    style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="#d3d3d3")

    table = ttk.Treeview(
        table_frame,
        columns=("User", "Recipes Added"),
        show="headings",
        style="Treeview",
    )
    table.heading("User", text="User")
    table.heading("Recipes Added", text="Recipes Added")
    table.column("User", anchor="w", width=200)
    table.column("Recipes Added", anchor="center", width=150)

    # Insert data into the table
    for row in insights["user_recipe_data"]:
        table.insert("", "end", values=(row["user_name"], row["recipe_count"]))

    # Add vertical and horizontal scrollbars
    scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    scrollbar_y.pack(side="right", fill="y")
    table.configure(yscrollcommand=scrollbar_y.set)

    table.pack(fill="both", expand=True)

    ### Visualization 4: Bar Chart - Recipes by Time Taken ###
    time_chart_frame = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=10)
    time_chart_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

    fig3, ax3 = plt.subplots(figsize=(5, 3))
    ax3.bar(
        [d["time_range"] for d in insights["time_data"]],
        [d["count"] for d in insights["time_data"]],
        color="lightgreen",
    )
    ax3.set_title("Recipes by Time Taken", fontsize=14)
    ax3.set_xlabel("Time Ranges", fontsize=12)
    ax3.set_ylabel("Number of Recipes", fontsize=12)
    fig3.tight_layout()

    chart3 = FigureCanvasTkAgg(fig3, master=time_chart_frame)
    chart3.get_tk_widget().pack(fill="both", expand=True)



    ### Save-As-Image Button ###
    def save_as_image():
        # Get the bounding box of the current window
        x = admin_root.winfo_rootx()
        y = admin_root.winfo_rooty()
        width = admin_root.winfo_width()
        height = admin_root.winfo_height()

        # Grab the screenshot of the current window
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))

        # Generate a file name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"dashboard_{timestamp}.png"

        # Save the file in the same directory as the script
        script_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_directory, file_name)

        # Save the screenshot
        screenshot.save(file_path)
        messagebox.showinfo("Success", f"Dashboard saved as an image at {file_path}")

    save_button = ctk.CTkButton(
        content_frame,
        text="Save Dashboard as Image",
        command=save_as_image
    )
    save_button.grid(row=3, column=0, columnspan=1, pady=20)

    insights = admin_utils.get_insights()
    if not insights:
        messagebox.showerror("Error", "Failed to fetch insights")
        return

    # Display Insights and Analytics
    ctk.CTkLabel(content_frame, text="Analytics Insights",corner_radius=40, font=("Arial", 16, "bold")).pack(pady=10)

    def generate_report():
        admin_utils.generate_pdf_with_visuals(username, insights)

    # Button to download report
    ctk.CTkButton(
        content_frame,
        text="Download PDF Report",
        command=generate_report,
        width=200,
        height=40
    ).pack(pady=20)


# Generate Reports
def generate_reports(content_frame, username = ''):
    """
    DESC:
        Generates analytics reports for the admin. Provides options to download or view the reports.

    :param content_frame: CTkFrame, the content area frame for displaying report options.
    :param username: str, Optional, the username of the logged-in admin.
    :return: None
    """
    for widget in content_frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(content_frame, text="Generate Analytics Report", font=("Arial", 18, "bold")).pack(pady=10)
    
    # Add a button for generating the analytics report
    ctk.CTkButton(
        content_frame,
        text="Cook-Mate Analytics Report",
        command=lambda: admin_utils.generate_analytics_report_with_formatting(username)
    ).pack(pady=10)

def add_recipe(content_frame):
    """
    DESC:
        Displays a form for adding a new recipe with fields like name, ingredients, procedure, and more.
        Saves the recipe to the database upon submission.

    :param content_frame: CTkFrame, the content area frame for displaying the add recipe form.
    :return: None
    """
    for widget in content_frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(content_frame, text="Add New Recipe", font=("Arial", 18, "bold")).pack(pady=10)

    fields = {
        "Name": "",
        "Ingredients (comma-separated)": "",
        "Procedure (Steps)": "",  # Updated label
        "Dietary Condition": "",
        "Time Taken (in minutes)": "",
        "YouTube Link (optional)": ""
    }

    entries = {}
    for label, _ in fields.items():
        frame = ctk.CTkFrame(content_frame, fg_color="white")
        frame.pack(pady=5, padx=10, fill="x")
        ctk.CTkLabel(frame, text=label, font=("Arial", 14)).pack(side="top", padx=10, anchor="w")

        # Use CTkTextbox for the "Procedure" field
        if label == "Procedure (Steps)":
            text_widget = ctk.CTkTextbox(frame, width=400, height=100)  # Set appropriate size
            text_widget.pack(side="top", padx=10, pady=5, fill="x")
            entries[label] = text_widget
        else:
            entry = ctk.CTkEntry(frame, width=400)
            entry.pack(side="top", padx=10, pady=5, fill="x")
            entries[label] = entry

    def save_new_recipe():
        # Get values from entry fields, handle CTkTextbox separately
        new_recipe = {
            label: entry.get("1.0", "end-1c") if isinstance(entry, ctk.CTkTextbox) else entry.get()
            for label, entry in entries.items()
        }
        try:
            admin_utils.add_recipe_to_db(new_recipe)
            messagebox.showinfo("Success", "Recipe added successfully!")
            manage_recipes(content_frame)  # Refresh the recipe management view
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add recipe: {e}")

    ctk.CTkButton(content_frame, text="Save Recipe", command=save_new_recipe).pack(pady=20)


if __name__ == "__main__":
    show_admin_dashboard()
