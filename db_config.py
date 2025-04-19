import mysql.connector
from mysql.connector import Error
import random

def generate_food_quote():
    food_quotes = [
        "People who love to eat are always the best people. – Julia Child",
        "Food is symbolic of love when words are inadequate. – Alan D. Wolfelt",
        "Good food is the foundation of genuine happiness. – Auguste Escoffier",
        "Life is uncertain. Eat dessert first. – Ernestine Ulmer",
        "One cannot think well, love well, sleep well, if one has not dined well. – Virginia Woolf",
        "Cooking is like love. It should be entered into with abandon or not at all. – Harriet Van Horne",
        "There is no sincerer love than the love of food. – George Bernard Shaw",
        "Food is the ingredient that binds us together.",
        "A recipe has no soul. You, as the cook, must bring soul to the recipe. – Thomas Keller",
        "You don’t need a silver fork to eat good food. – Paul Prudhomme",
        "First we eat, then we do everything else. – M.F.K. Fisher",
        "The secret ingredient is always love.",
        "Eat breakfast like a king, lunch like a prince, and dinner like a pauper. – Adelle Davis",
        "Happiness is homemade.",
        "Food is not just fuel. It’s about family, culture, and identity. – Michael Pollan",
        "An empty belly is the best cook. – Estonian Proverb",
        "Food brings people together on many different levels. It's nourishment of the soul and body; it’s truly love. – Giada De Laurentiis",
        "The belly rules the mind. – Spanish Proverb",
        "Cooking is an art, but all art requires knowing something about the techniques and materials. – Nathan Myhrvold",
        "You can’t live a full life on an empty stomach."
    ]
    return random.choice(food_quotes)

"""
Database Utilities for Cook Mate

This module provides functions for database connectivity, schema initialization, and query execution for the Cook Mate application.

Functions:
- `create_connection`: Establishes a connection to the database and ensures tables are initialized.
- `close_connection`: Closes the database connection if it is open.
- `centre_window`: Centers a GUI window on the screen.
- `initialize_tables`: Creates required tables in the database if they do not already exist.
- `insert_recipe`: Inserts a new recipe into the Recipes table.
- `execute_query`: Executes a parameterized SQL query with the provided parameters.
"""
DB_CONFIG = {
    "host": "141.209.241.57",
    "user": "gundl2a",
    "password": "mypass",
    "database": "BIS698W_GRP1"
}

# Function to create a connection to the database
def create_connection():
    """
    DESC:
        Establishes a connection to the MySQL database using the provided credentials. Ensures required tables 
        are initialized if they do not exist.

    :param: None
    :return: mysql.connector.connection.MySQLConnection or None, A database connection object or None if connection fails.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            initialize_tables(connection)  # Ensuring tables are created if they don't exist
            return connection
    except Error as e:
        print(f"Error: '{e}'")
    return None

# Function to close the database connection
def close_connection(connection):
    """
    DESC:
        Closes an open database connection.

    :param connection: mysql.connector.connection.MySQLConnection, The connection object to close.
    :return: None
    """
    if connection and connection.is_connected():
        connection.close()

# Center the window on the screen

def centre_window(window, width=None, height=None):
    """
    Center the window on the screen.
    
    Parameters:
        window: The Tkinter window to center.
        width: Optional width of the window. If None, use current window width.
        height: Optional height of the window. If None, use current window height.
    """
    window.update_idletasks()  # Ensure dimensions are calculated
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Use current width and height if not specified
    window_width = width or window.winfo_width()
    window_height = height or window.winfo_height()
    
    # Calculate position x, y
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Function to initialize required tables
def initialize_tables(connection):
    """
    DESC:
        Creates the `Recipes` and `Users` tables in the database if they do not already exist.

    :param connection: mysql.connector.connection.MySQLConnection, The database connection object.
    :return: None
    """

    create_recipe_table_query = """
    CREATE TABLE IF NOT EXISTS Recipes (
        recipe_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        ingredients TEXT NOT NULL,
        steps TEXT NOT NULL,
        dietary_condition VARCHAR(50) NOT NULL,
        time_taken VARCHAR(50) NOT NULL,
        youtube_link VARCHAR(255)      -- Optional
    )
    """
    create_users_table_query = """
    CREATE TABLE IF NOT EXISTS Users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        phone_number VARCHAR(50),
        email VARCHAR(255) NOT NULL UNIQUE,
        dietary_preference VARCHAR(50),
        role VARCHAR(50) DEFAULT 'user')"""
    cursor = connection.cursor()
    try:
        cursor.execute(create_recipe_table_query)
        cursor.execute(create_users_table_query)
        connection.commit()
        print("Tables initialized successfully.")
    except Error as e:
        print(f"Error initializing tables: '{e}'")
    finally:
        cursor.close()

# Function to insert recipe details into the database
def insert_recipe(data):
    """
    DESC:
        Inserts a new recipe into the Recipes table.

    :param data: tuple, A tuple containing recipe details (name, ingredients, steps, dietary_condition, time_taken, youtube_link, user_id).
    :return: None
    """

    query = """
    INSERT INTO Recipes (name, ingredients, steps, dietary_condition, time_taken, youtube_link, user_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query, data)
            connection.commit()
            print("Recipe added successfully!")
        except Error as e:
            print(f"Error inserting recipe data: '{e}'")
        finally:
            close_connection(connection)

def execute_query(query, params):
    """
    DESC:
        Executes a parameterized SQL query with the provided parameters.

    :param query: str, The SQL query to execute.
    :param params: tuple, The parameters to use in the query.
    :return: None
    """
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            print("Query executed successfully!")
        except Error as e:
            print(f"Error executing the query: '{e}'")
        finally:
            close_connection(connection)