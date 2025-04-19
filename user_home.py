import customtkinter as ctk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
from tkinter import HORIZONTAL, VERTICAL, Canvas, Scrollbar
import login_screen  # Import login screen for navigation on logout
import db_config  # Import database configuration and operations

"""
User Home Screen Functions

This module provides the functionality for the user home screen of the Cook Mate application. It includes features 
for viewing, adding, and searching recipes, as well as logging out. Each functionality is displayed within a 
well-structured layout with a sidebar for navigation.

Functions:
- `show_user_home`: Initializes and displays the main user home screen.
- `show_user_home_content`: Displays the initial content on the user home screen.
- `search_recipe`: Allows users to search for recipes with filters for dietary conditions and time taken.
- `add_recipe_form`: Displays a form for users to add a new recipe.
- `view_my_recipes`: Displays all recipes added by the logged-in user.
- `logout`: Logs out the user and redirects to the login screen.

- In `search_recipe`:
  - `perform_search`: Executes the search query based on filters and displays the results.
  - `download_as_pdf`: Downloads a recipe as a PDF file.

- In `add_recipe_form`:
  - `submit_recipe`: Submits the new recipe data to the database.

- In `show_user_home`:
  - `on_button_click`: Executes the command associated with a sidebar button click.
"""


# Function to show search recipe window with filters and results
def search_recipe(content_frame):
    """
    Displays the search recipe interface with filters and results.

    This function creates a search bar, filters for dietary concerns and time taken,
    and a search button. It also sets up a scrollable frame to display search results.

    Args:
        content_frame (ctk.CTkFrame): The frame where the search interface will be displayed.

    Returns:
        None
    """
    # Clear the content frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Title for the search recipe window
    search_title = ctk.CTkLabel(content_frame, text="Search Recipes", font=("Arial", 24), text_color="black")
    search_title.pack(pady=10)

    # Search bar
    search_frame = ctk.CTkFrame(content_frame, fg_color="white")
    search_frame.pack(pady=10, fill="x", padx=10)

    search_label = ctk.CTkLabel(search_frame, text="Search by name or ingredient:", font=("Arial", 12), text_color="black")
    search_label.grid(row=0, column=0, padx=5, pady=5)

    search_entry = ctk.CTkEntry(search_frame, width=300, placeholder_text="Enter recipe name or ingredient")
    search_entry.grid(row=0, column=1, padx=5, pady=5)

    # Filters for dietary concerns and time taken
    filter_frame = ctk.CTkFrame(content_frame, fg_color="white")
    filter_frame.pack(pady=10, fill="x", padx=10)

    dietary_label = ctk.CTkLabel(filter_frame, text="Dietary Concern:", font=("Arial", 12), text_color="black")
    dietary_label.grid(row=0, column=0, padx=5, pady=5)

    dietary_options = ["Any", "Vegan", "Vegetarian", "Non-Vegetarian", "Gluten-Free"]
    dietary_filter = ctk.CTkComboBox(filter_frame, values=dietary_options)
    dietary_filter.grid(row=0, column=1, padx=5, pady=5)
    dietary_filter.set("Any")  # Default option

    time_label = ctk.CTkLabel(filter_frame, text="Time Taken:", font=("Arial", 12), text_color="black")
    time_label.grid(row=0, column=2, padx=5, pady=5)

    # Time Taken Filter Dropdown
    time_options = ["Any", "Less than 15 min", "Less than 30 min", "More than 30 min", "Instant"]
    time_filter = ctk.CTkComboBox(filter_frame, values=time_options)
    time_filter.grid(row=0, column=3, padx=5, pady=5)
    time_filter.set("Any")  # Default option

    # Search button
    from tkinter import HORIZONTAL, VERTICAL, Canvas, Scrollbar

    def perform_search():
        """
    Executes the recipe search based on user input and displays results.

    This function retrieves search parameters, constructs an SQL query with filters,
    executes the query, and displays the results in a scrollable frame. It also
    provides a "Download as PDF" option for each recipe.

    Args:
        None

    Returns:
        None
    """
    # Clear previous results
        for widget in results_frame.winfo_children():
            widget.destroy()

        # Create a Canvas for scrolling
        canvas = Canvas(results_frame, bg="white")
        canvas.pack(side="left", fill="both", expand=True)

        v_scrollbar = Scrollbar(results_frame, orient=VERTICAL, command=canvas.yview)
        v_scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=v_scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        scrollable_frame = ctk.CTkFrame(canvas, fg_color="white")
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Get search parameters
        search_term = search_entry.get().strip()
        dietary_concern = dietary_filter.get()
        time_taken = time_filter.get()

        # Split multiple ingredients by comma
        ingredients = [ingredient.strip() for ingredient in search_term.split(",") if ingredient.strip()]

        # Construct the SQL query
        query = "SELECT * FROM Recipes WHERE (1=1)"
        params = []

        if ingredients:
            for ingredient in ingredients:
                query += " OR ingredients LIKE %s "
                params.append(f"%{ingredient}%")

        if dietary_concern != "Any":
            query += " AND dietary_condition = %s"
            params.append(dietary_concern)

        if time_taken != "Any":
            if time_taken == "Less than 15 min":
                query += " AND time_taken <= 15"
            elif time_taken == "Less than 30 min":
                query += " AND time_taken > 15 AND time_taken <= 30"
            elif time_taken == "More than 30 min":
                query += " AND time_taken > 30"
            elif time_taken == "Instant":
                query += " AND time_taken = 0"
        # #Initialize query and parameters
        # query = "SELECT * FROM Recipes WHERE (1=1) "  # Base query
        # params = []

        # # Filter by ingredients
        # if ingredients:
        #     for ingredient in ingredients:
        #         query += " ingredients LIKE %s"
        #         params.append(f"%{ingredient}%")
        # if ingredients:
        #     for ingredient in ingredients:
        #         query += " OR name LIKE %s"
        #         params.append(f"%{ingredient}%")        

        # Ensure dietary_concern is always considered
        if dietary_concern == "Any":
            query += " AND dietary_condition IS NOT NULL"  # Include recipes with any dietary condition
        else:
            query += " AND dietary_condition = %s"
            params.append(dietary_concern)

        # Ensure time_taken is always considered
        if time_taken == "Any":
            query += " AND time_taken IS NOT NULL"  # Include recipes with any time_taken
        else:
            if time_taken == "Less than 15 min":
                query += " AND time_taken <= 15"
            elif time_taken == "Less than 30 min":
                query += " AND time_taken > 15 AND time_taken <= 30"
            elif time_taken == "More than 30 min":
                query += " AND time_taken > 30"
            elif time_taken == "Instant":
                query += " AND time_taken = 0"


        connection = db_config.create_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, tuple(params))
                results = cursor.fetchall()
                if results:
                    # Display search results
                    for recipe in results:
                        recipe_title = ctk.CTkLabel(
                            scrollable_frame,
                            text=recipe['name'],
                            font=("Arial", 18, "bold"),
                            text_color="black"
                        )
                        recipe_title.pack(pady=10, anchor="w")

                        details = f"""
                        Dietary Condition: {recipe['dietary_condition']}
                        Time Taken: {recipe['time_taken']} minutes
                        Ingredients: {recipe['ingredients']}
                        Cooking Steps: {recipe['steps']}
                        YouTube Link: {recipe.get('youtube_link', 'Not specified')}
                        """
                        recipe_details = ctk.CTkLabel(
                            scrollable_frame,
                            text=details,
                            font=("Arial", 12),
                            justify="left",
                            text_color="black",
                            wraplength=800
                        )
                        recipe_details.pack(pady=5, anchor="w")

                        def download_as_pdf(recipe=recipe):
                            """
                            Generates a PDF file for a given recipe.

                            This function creates a PDF document containing all the details of a recipe,
                            including name, dietary condition, time taken, ingredients, cooking steps,
                            and YouTube link.

                            Args:
                                recipe (dict): A dictionary containing recipe details.

                            Returns:
                                None
                            """
                            from fpdf import FPDF
                            pdf = FPDF()
                            pdf.add_page()
                            pdf.set_font("Arial", size=12)
                            pdf.cell(200, 10, txt=recipe['name'], ln=True, align="C")
                            pdf.ln(10)
                            pdf.multi_cell(0, 10, f"Dietary Condition: {recipe['dietary_condition']}\n"
                                                f"Time Taken: {recipe['time_taken']} minutes\n"
                                                f"Ingredients: {recipe['ingredients']}\n"
                                                f"Cooking Steps: {recipe['steps']}\n"
                                                f"YouTube Link: {recipe['youtube_link']}\n")
                            pdf.output(f"{recipe['name']}.pdf")
                            messagebox.showinfo("Download", "Recipe downloaded as .pdf")

                        pdf_button = ctk.CTkButton(
                            scrollable_frame,
                            text="Download as PDF",
                            command=lambda recipe=recipe: download_as_pdf(recipe)
                        )
                        pdf_button.pack(pady=5, anchor="w")
                else:
                    no_results_label = ctk.CTkLabel(scrollable_frame, text="No recipes found.", font=("Arial", 14),
                                                    text_color="black")
                    no_results_label.pack(pady=5, anchor="w")
            except Exception as e:
                messagebox.showerror("Error", f"Error performing search: {e}")
            finally:
                db_config.close_connection(connection)


    search_button = ctk.CTkButton(content_frame, text="Search", font=("Arial", 12), command=perform_search)
    search_button.pack(pady=10)

    # Results frame for displaying search results
    results_frame = ctk.CTkFrame(content_frame, fg_color="white")
    results_frame.pack(fill="both", expand=True, padx=10, pady=10)


# Function to add a recipe
def add_recipe_form(content_frame, user_id):
    """
    Displays a form for adding a new recipe.

    This function creates input fields for recipe details such as name, ingredients,
    cooking steps, dietary condition, time taken, and YouTube link. It also includes
    a submit button to add the recipe to the database.

    Args:
        content_frame (ctk.CTkFrame): The frame where the form will be displayed.
        user_id (int): The ID of the current user.

    Returns:
        None
    """
    # Clear the content frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Title for the Add Recipe window
    add_recipe_title = ctk.CTkLabel(content_frame, text="Add a New Recipe", font=("Arial", 24), text_color="black")
    add_recipe_title.pack(pady=10)

    # Frame for entry fields
    entry_frame = ctk.CTkFrame(content_frame, fg_color="white")
    entry_frame.pack(pady=10, padx=10, fill="x")

    # Labels and entry fields for each recipe attribute
    fields = [
        ("Recipe Name:", "Enter recipe name"),
        ("Ingredients (comma-separated):", "Enter ingredients"),
        ("YouTube Link (optional):", "Enter YouTube link")
    ]

    entries = {}
    for idx, (label_text, placeholder) in enumerate(fields):
        label = ctk.CTkLabel(entry_frame, text=label_text, font=("Arial", 12), text_color="black")
        label.grid(row=idx, column=0, padx=5, pady=5, sticky="w")

        entry = ctk.CTkEntry(entry_frame, width=400, placeholder_text=placeholder)
        entry.grid(row=idx, column=1, padx=10, pady=7)
        entries[label_text] = entry

    # Large text box for Cooking Steps
    steps_label = ctk.CTkLabel(entry_frame, text="Cooking Steps:", font=("Arial", 12), text_color="black")
    steps_label.grid(row=len(fields), column=0, padx=5, pady=5, sticky="w")
    steps_textbox = ctk.CTkTextbox(entry_frame, width=400, height=100, font=("Arial", 12))
    steps_textbox.grid(row=len(fields), column=1, padx=10, pady=7)

    # Dropdown for Dietary Condition
    diet_label = ctk.CTkLabel(entry_frame, text="Dietary Condition:", font=("Arial", 12), text_color="black")
    diet_label.grid(row=len(fields) + 1, column=0, padx=5, pady=5, sticky="w")
    diet_options = ["Vegetarian", "Non-Vegetarian", "Vegan", "Gluten-Free"]
    diet_dropdown = ctk.CTkComboBox(entry_frame, values=diet_options, width=400)
    diet_dropdown.grid(row=len(fields) + 1, column=1, padx=10, pady=7)
    diet_dropdown.set("Select Dietary Condition")  # Default value

    # Dropdown for Time Taken
    time_label = ctk.CTkLabel(entry_frame, text="Time Taken (mins):", font=("Arial", 12), text_color="black")
    time_label.grid(row=len(fields) + 2, column=0, padx=5, pady=5, sticky="w")
    time_options = ["Less than 15 min", "Less than 30 min", "More than 30 min", "Instant"]
    time_dropdown = ctk.CTkComboBox(entry_frame, values=time_options, width=400)
    time_dropdown.grid(row=len(fields) + 2, column=1, padx=10, pady=7)
    time_dropdown.set("Select Time")  # Default value

    # Function to submit the recipe to the database
    def submit_recipe():
        """
    Submits a new recipe to the database.

    This function collects data from the add recipe form, validates it, and inserts
    the new recipe into the database. It also handles error messages and clears the
    form after successful submission.

    Args:None

    Returns:None
    """
        # Get data from entry fields
        recipe_data = [
            entries["Recipe Name:"].get(),
            entries["Ingredients (comma-separated):"].get(),
            steps_textbox.get("1.0", 'end').strip(),  # Get text from the textbox
            diet_dropdown.get() if diet_dropdown.get() != "Select Dietary Condition" else None,
            time_dropdown.get() if time_dropdown.get() != "Select Time" else None,
            entries["YouTube Link (optional):"].get() or None,
            user_id  # Include user_id to map recipe to user
        ]

        # Check for mandatory fields
        if all(recipe_data[:4]):  # Ensure all required fields are filled
            try:
                connection = db_config.create_connection()
                if connection:
                    query = """
                        INSERT INTO Recipes (name, ingredients, steps, dietary_condition, time_taken, youtube_link, user_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor = connection.cursor()
                    cursor.execute(query, tuple(recipe_data))
                    connection.commit()
                    messagebox.showinfo("Success", "Recipe added successfully!")
                    # Clear fields after submission
                    for entry in entries.values():
                        entry.delete(0, 'end')
                    steps_textbox.delete("1.0", 'end')
                    diet_dropdown.set("Select Dietary Condition")
                    time_dropdown.set("Select Time")
            except Exception as e:
                messagebox.showerror("Error", f"Error adding recipe: {e}")
            finally:
                db_config.close_connection(connection)
        else:
            messagebox.showwarning("Warning", "Please fill in all mandatory fields!")

    # Submit button
    submit_button = ctk.CTkButton(content_frame, text="Add Recipe", font=("Arial", 12), command=submit_recipe)
    submit_button.pack(pady=20)


def view_my_recipes(content_frame, user_id):
    """
    Displays all recipes added by the current user.

    This function retrieves all recipes associated with the user_id from the database
    and displays them in a scrollable frame. Each recipe is shown with its details.

    Args:
        content_frame (ctk.CTkFrame): The frame where recipes will be displayed.
        user_id (int): The ID of the current user.

    Returns:
        None
    """
    connection = db_config.create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM Recipes WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()

            # Clear existing widgets in the content frame
            for widget in content_frame.winfo_children():
                widget.destroy()

            if results:
                canvas = Canvas(content_frame, bg="white", highlightthickness=5)
                scrollable_frame = ctk.CTkFrame(canvas, fg_color="white")

                h_scrollbar = Scrollbar(content_frame, orient=HORIZONTAL, command=canvas.xview)
                v_scrollbar = Scrollbar(content_frame, orient=VERTICAL, command=canvas.yview)

                canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)

                canvas.pack(side="left", fill="both", expand=True)
                v_scrollbar.pack(side="right", fill="y")
                h_scrollbar.pack(side="bottom", fill="x")

                canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

                # Use a grid layout for recipes
                for idx, recipe in enumerate(results):
                    recipe_frame = ctk.CTkFrame(scrollable_frame, fg_color="white")
                    recipe_frame.grid(row=idx, column=0, padx=10, pady=10, sticky="ew")

                    title_label = ctk.CTkLabel(
                        recipe_frame, 
                        text=recipe['name'], 
                        font=("Arial", 18, "bold"), 
                        text_color="black"
                    )
                    title_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

                    content_text = f"""
Dietary Condition: {recipe['dietary_condition']}
Ingredients: {recipe.get('ingredients', 'Not specified')}
Steps: {recipe.get('steps', 'Not specified')}
YouTube Link: {recipe.get('youtube_link', 'Not specified')}
"""
                    content_label = ctk.CTkLabel(
                        recipe_frame, 
                        text=content_text.strip(), 
                        font=("Arial", 14), 
                        text_color="black", 
                        justify="left", 
                        wraplength=700
                    )
                    content_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

                    # Divider for better visibility
                    divider = ctk.CTkLabel(recipe_frame, text="-" * 50, text_color="gray")
                    divider.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

                # Update the scrollable area
                scrollable_frame.update_idletasks()
                canvas.config(scrollregion=canvas.bbox("all"))
            else:
                messagebox.showinfo("Info", "No recipes found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving recipes: {e}")
        finally:
            db_config.close_connection(connection)



# Function to log out and navigate to the login screen
def logout():
    """
    Logs out the current user and returns to the homepage.

    This function closes the current user home screen and opens the application's
    homepage.

    Args:
        None

    Returns:
        None
    """
    root.destroy()  # Close the user home screen
    import app
    app.show_homepage()
# Function to show the user home screen content
def show_user_home_content(content_frame, user_id, username):
    """
    DESC:
        Displays the initial content on the user home screen, including a welcome message and action buttons.

    :param content_frame: CTkFrame, The frame to display the content in.
    :param user_id: int, The unique ID of the logged-in user.
    :param username: str, The username of the logged-in user.
    :return: None
    """
    # Clear any existing widgets in the content frame
    for widget in content_frame.winfo_children():
        widget.destroy()
    icon_path = "Assets/logo.png"  # Path to your Cook Mate icon
    cookmate_icon = ctk.CTkImage(
    light_image=Image.open(icon_path),
    size=(250, 250)  # Adjust the size of the icon as needed
    )
    active_user_label = ctk.CTkLabel(content_frame,
    image=cookmate_icon,  # Set the icon
    text=f"{username}",  # Display only the username
    font=("Arial", 16, "bold"),
    text_color="white",
    compound="top",  # Place the icon above the username
    justify="center"
    )
    active_user_label.pack(pady=20)
   

    # Display Welcome message
    welcome_label = ctk.CTkLabel(content_frame, text=f"Welcome to CookMate, {username} ",
                                 font=("Arial", 24), text_color='black')
    welcome_label.pack(pady=20)

    # Sidebar buttons and labels configuration
    button_config = [
        ("Assets/view_icon.png", "My Recipes", lambda: view_my_recipes(content_frame, user_id)),
        ("Assets/add_icon.png", "Add Recipe", lambda: add_recipe_form(content_frame, user_id)),
        ("Assets/search_icon.png", "Search Recipes", lambda: search_recipe(content_frame)),
        ("Assets/logout_icon.png", "Logout", logout)
    ]

    # Create buttons with icons and labels in the main content frame
    for icon_path, label_text, command in button_config:
        icon = Image.open(icon_path)
        icon = icon.resize((40, 40), Image.Resampling.LANCZOS)
        icon_photo = ImageTk.PhotoImage(icon)

        button_frame = ctk.CTkFrame(content_frame, fg_color="white")
        button_frame.pack(pady=10)

        icon_label = ctk.CTkLabel(button_frame, image=icon_photo, text="")
        icon_label.image = icon_photo  # Prevent garbage collection
        icon_label.pack()

        text_label = ctk.CTkButton(button_frame, text=label_text, fg_color="white", text_color="black",
                                   font=("Arial", 12), command=command)
        text_label.pack()


def show_user_home(user_id, username):
    """
    DESC:
        Initializes and displays the main user home screen with a sidebar for navigation and a content frame 
        for displaying features like viewing, adding, and searching recipes.

    :param user_id: int, The unique ID of the logged-in user.
    :param username: str, The username of the logged-in user.
    :return: None
    """
    global root
    root = ctk.CTk()
    root.title("CookMate")
    root.geometry("1200x700")

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # Main layout: divide window into two parts
    root.grid_columnconfigure(0, weight=1)  # Left column (sidebar frame)
    root.grid_columnconfigure(1, weight=6)  # Right column (content display)
    root.grid_rowconfigure(0, weight=1)     # Ensure the row expands with the window

    # Sidebar Frame
    sidebar_frame = ctk.CTkFrame(root, fg_color="#003366", width=100)  # Blue background
    sidebar_frame.grid(row=0, column=0, sticky="nsew")  # Expand vertically

    # Content Frame
    content_frame = ctk.CTkFrame(root, fg_color="white")
    content_frame.grid(row=0, column=1, sticky="nsew")  # Fill the remaining space

    # Sidebar Buttons
    def on_button_click(command):
        command()  # Execute the command passed from the button
    
    button_config = [
        ("Assets/view_icon.png", "View Recipes", lambda: view_my_recipes(content_frame, user_id)),
        ("Assets/add_icon.png", "Add Recipe", lambda: add_recipe_form(content_frame, user_id)),
        ("Assets/search_icon.png", "Search Recipes", lambda: search_recipe(content_frame)),
        ("Assets/logout_icon.png", "Logout", logout)
    ]

    for icon_path, label_text, command in button_config:
        # Load and resize icon
        icon = Image.open(icon_path)
        icon = icon.resize((40, 40), Image.Resampling.LANCZOS)
        icon_photo = ImageTk.PhotoImage(icon)

        # Create a frame for each button with an icon and label
        button_frame = ctk.CTkFrame(sidebar_frame, fg_color="#ffffff") 
        button_frame.pack(pady=10, padx=5, fill="x")

        # Add icon to the frame
        icon_label = ctk.CTkLabel(button_frame, image=icon_photo, text="", fg_color="#ffffff")
        icon_label.image = icon_photo  # Prevent garbage collection
        icon_label.pack(side="left", padx=10)

        # Add button to the frame
        text_button = ctk.CTkButton(
            button_frame, text=label_text, fg_color="#ffffff",width=150, text_color="#00008B",corner_radius=35, 
            font=("Cooper Hewitt Heavy", 14), hover_color="#4682B4",  # Slightly darker hover color
            command=lambda cmd=command: on_button_click(cmd)
        )
        text_button.pack(side="left", fill="x", expand=True)

    # Display initial content in the right frame
    show_user_home_content(content_frame, user_id, username)

    # Ensure the sidebar and content frame resize with the root window
    root.update_idletasks()
    root.mainloop()
