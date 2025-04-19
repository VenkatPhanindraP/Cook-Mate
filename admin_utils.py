from binascii import Error
import db_config
import os
from io import BytesIO
from db_config import create_connection, close_connection 
from tkinter import messagebox
from fpdf import FPDF
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import matplotlib.pyplot as plt
import customtkinter as ctk
import admin_dashboard


def popup_authentication(action, user_id=None, new_role=None, content_frame=None):
    """
    Displays a visually enhanced popup window to authenticate admin credentials.

    :param action: str, The action to perform after authentication ("delete" or "change_role").
    :param user_id: int, The user ID for deletion (if applicable).
    :param new_role: str, The new role to set for the user (if applicable).
    :param content_frame: CTkFrame, The content frame for refreshing the view post-action.
    :return: None
    """
    def authenticate_and_proceed():
        username = username_entry.get()
        password = password_entry.get()

        if username in ["Admin", "admin"] and password == "Admin@123":
            auth_window.destroy()  # Close the authentication window

            if action == "delete":
                # Perform user deletion
                delete_user(user_id)
                messagebox.showinfo("Success", f"User ID {user_id} has been deleted.")
            elif action == "change_role":
                # Perform role change
                update_user_role(user_id, new_role)
                messagebox.showinfo("Success", f"Role updated to {new_role} for user ID {user_id}.")
            
            # Redirect to home page
            admin_dashboard.show_home_content(content_frame, username)  # Replace "Admin" with the actual username if needed.
        else:
            error_label.configure(text="Invalid credentials. Please try again.")

    # Create a new CTk Toplevel window for authentication
    auth_window = ctk.CTkToplevel()
    auth_window.title("Admin Authentication")
    auth_window.geometry("400x400")
    auth_window.resizable(False, False)

    auth_window.transient(content_frame)  # Set it as a child window of the main window
    auth_window.grab_set()  # Disable interaction with the main window until this window is closed
    auth_window.focus_set()

    # Set a clean and centered layout
    auth_frame = ctk.CTkFrame(auth_window, corner_radius=15, fg_color="#f7f7f7")
    auth_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Title Label
    title_label = ctk.CTkLabel(auth_frame, text="Admin Authentication", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Username label and entry
    username_label = ctk.CTkLabel(auth_frame, text="Admin Username:", font=("Arial", 14))
    username_label.pack(pady=5, anchor="w", padx=10)
    username_entry = ctk.CTkEntry(auth_frame, font=("Arial", 14), width=300)
    username_entry.pack(pady=5)

    # Password label and entry
    password_label = ctk.CTkLabel(auth_frame, text="Admin Password:", font=("Arial", 14))
    password_label.pack(pady=10, anchor="w", padx=10)
    password_entry = ctk.CTkEntry(auth_frame, font=("Arial", 14), show="*", width=300)
    password_entry.pack(pady=5)

    # Error Label
    error_label = ctk.CTkLabel(auth_frame, text="", font=("Arial", 12), text_color="red")
    error_label.pack(pady=5)

    # Save Changes Button
    save_button = ctk.CTkButton(
        auth_frame,
        text="Save Changes",
        font=("Arial", 14),
        width=150,
        height=40,
        command=authenticate_and_proceed,
        corner_radius=10
    )
    save_button.pack(pady=20)

    # Cancel Button
    cancel_button = ctk.CTkButton(
        auth_frame,
        text="Cancel",
        font=("Arial", 14),
        width=150,
        height=40,
        fg_color="gray",
        hover_color="#b3b3b3",
        command=auth_window.destroy,
        corner_radius=10
    )
    cancel_button.pack()


def authenticate_admin():
    """
    Opens a visually aesthetic dialog to authenticate the admin before performing critical actions.
    :return: bool, True if authentication is successful, otherwise False.
    """
    auth_window = ctk.CTkToplevel()
    auth_window.title("Admin Authentication")
    auth_window.geometry("500x300")
    auth_window.resizable(False, False)
    auth_window.grab_set()  # Disable interaction with other windows
    auth_window.focus_set()
    auth_window.configure(fg_color="#f9f9f9")  # Light gray background

    # Header Label
    header_label = ctk.CTkLabel(
        auth_window,
        text="Admin Authentication",
        font=("Arial", 20, "bold"),
        fg_color="#3B82F6",
        text_color="white",
        corner_radius=8,
        height=40
    )
    header_label.pack(fill="x", pady=(10, 20))

    # Form Frame
    form_frame = ctk.CTkFrame(auth_window, fg_color="#ffffff", corner_radius=10)
    form_frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Username Label and Entry
    ctk.CTkLabel(
        form_frame, text="Admin Username:", font=("Arial", 14), anchor="w"
    ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
    username_entry = ctk.CTkEntry(form_frame, font=("Arial", 12), width=250)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    # Password Label and Entry
    ctk.CTkLabel(
        form_frame, text="Admin Password:", font=("Arial", 14), anchor="w"
    ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    password_entry = ctk.CTkEntry(form_frame, font=("Arial", 12), show="*", width=250)
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    auth_result = {"success": False}  # Store the authentication result

    def verify_credentials():
        username = username_entry.get()
        password = password_entry.get()
        if username.lower() == "admin" and password == "Admin@123":
            auth_result["success"] = True
            messagebox.showinfo("Authentication", "Admin authenticated successfully.")
            auth_window.destroy()
        else:
            messagebox.showerror("Authentication Failed", "Invalid admin credentials.")

    # Buttons Frame
    buttons_frame = ctk.CTkFrame(auth_window, fg_color="#f9f9f9")
    buttons_frame.pack(pady=10)

    # Login Button
    ctk.CTkButton(
        buttons_frame,
        text="Save Changes",
        font=("Arial", 14, "bold"),
        command=verify_credentials,
        fg_color="#10B981",
        hover_color="#059669",
        corner_radius=8,
        width=120,
        height=40
    ).grid(row=0, column=0, padx=10, pady=10)

    # Cancel Button
    ctk.CTkButton(
        buttons_frame,
        text="Cancel",
        font=("Arial", 14, "bold"),
        command=auth_window.destroy,
        fg_color="#EF4444",
        hover_color="#DC2626",
        corner_radius=8,
        width=120,
        height=40
    ).grid(row=0, column=1, padx=10, pady=10)

    auth_window.wait_window()  # Wait until the window is closed
    return auth_result["success"]


# Fetch all recipes
def get_all_recipes():
    connection = db_config.create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Recipes")
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching recipes: {e}")
        finally:
            db_config.close_connection(connection)


# Fetch all users
def get_all_users():
    connection = db_config.create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Users")
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching users: {e}")
        finally:
            db_config.close_connection(connection)


# Update a recipe
def update_recipe(updated_values):
    connection = db_config.create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                UPDATE Recipes
                SET name = %s, ingredients = %s, steps = %s, dietary_condition = %s,
                    time_taken = %s, youtube_link = %s
                WHERE recipe_id = %s
            """
            cursor.execute(query, (
                updated_values['Name'], updated_values['Ingredients'], updated_values['Procedure'],
                updated_values['Dietary Condition'], updated_values['Time Taken'],
                updated_values['YouTube Link'], updated_values['recipe_id']
            ))
            connection.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating recipe: {e}")
        finally:
            db_config.close_connection(connection)


# Delete a recipe
def delete_recipe(recipe_id):
    connection = db_config.create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Recipes WHERE recipe_id = %s", (recipe_id,))
            connection.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting recipe: {e}")
        finally:
            db_config.close_connection(connection)


# Update a user's role
def update_user_role(user_id, new_role):
    connection = db_config.create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE Users SET role = %s WHERE user_id = %s", (new_role, user_id))
            connection.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating user role: {e}")
        finally:
            db_config.close_connection(connection)


# Delete a user
def delete_user(user_id):
    connection = db_config.create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
            connection.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting user: {e}")
        finally:
            db_config.close_connection(connection)

def add_recipe_to_db(recipe_details):
    connection = db_config.create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO Recipes (name, ingredients, steps, dietary_condition, time_taken, youtube_link)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                recipe_details["Name"],
                recipe_details["Ingredients (comma-separated)"],
                recipe_details["Procedure"],
                recipe_details["Dietary Condition"],
                recipe_details["Time Taken (in minutes)"],
                recipe_details["YouTube Link (optional)"]
            ))
            connection.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding recipe to database: {e}")
        finally:
            db_config.close_connection(connection)


# Fetch insights
def get_insights():
    connection = db_config.create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)  # Initialize cursor here

            # Fetch total active users
            cursor.execute("SELECT COUNT(*) AS total_users FROM Users")
            total_users = cursor.fetchone()["total_users"]

            # Fetch total recipes
            cursor.execute("SELECT COUNT(*) AS total_recipes FROM Recipes")
            total_recipes = cursor.fetchone()["total_recipes"]

            # 1. Number of Recipes by Dietary Conditions
            cursor.execute("SELECT dietary_condition, COUNT(*) AS count FROM Recipes GROUP BY dietary_condition")
            diet_data = cursor.fetchall()

            # 2. Distribution of Users by Dietary Preferences
            cursor.execute("SELECT dietary_preference, COUNT(*) AS count FROM Users GROUP BY dietary_preference")
            user_diet_data = cursor.fetchall()

            # 3. Users vs. Number of Recipes Added
            cursor.execute("""
                SELECT 
                    u.username AS user_name, 
                    COUNT(r.recipe_id) AS recipe_count
                FROM Users u 
                LEFT JOIN Recipes r ON u.user_id = r.user_id
                GROUP BY u.username
                ORDER BY recipe_count DESC;
            """)
            user_recipe_data = cursor.fetchall()

            # 4. Recipes by Time Taken
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN time_taken <= 15 THEN '<15 min'
                        WHEN time_taken > 15 AND time_taken <= 30 THEN '15-30 min'
                        WHEN time_taken > 30 AND time_taken <= 60 THEN '30-60 min'
                        ELSE '>60 min'
                    END AS time_range, 
                    COUNT(*) AS count
                FROM Recipes
                GROUP BY time_range
                ORDER BY FIELD(time_range, '<15 min', '15-30 min', '30-60 min', '>60 min')
            """)
            time_data = cursor.fetchall()

            # Prepare the result dictionary
            return {
                "total_users": total_users,
                "total_recipes": total_recipes,
                "dietary_conditions": [d["dietary_condition"] for d in diet_data],
                "counts": [d["count"] for d in diet_data],
                "user_dietary_preferences": [d["dietary_preference"] for d in user_diet_data],
                "user_diet_counts": [d["count"] for d in user_diet_data],
                "user_recipe_data": user_recipe_data,
                "time_data": time_data
            }
        except Exception as e:
            print(f"Error fetching insights: {e}")
            return None
        finally:
            db_config.close_connection(connection)


def download_insights_image(dietary_conditions, counts, time_data, user_recipe_data):
    # Ask the user to choose a directory to save the images
    folder_path = filedialog.askdirectory(title="Select Folder to Save Insights")
    if not folder_path:
        return  # Exit if the user cancels

    try:
        # Save the dietary conditions bar chart
        fig1, ax1 = plt.subplots(figsize=(5, 3))
        ax1.bar(dietary_conditions, counts, color='skyblue')
        ax1.set_title("Recipes by Dietary Conditions", fontsize=14)
        ax1.set_xlabel("Dietary Conditions", fontsize=12)
        ax1.set_ylabel("Count", fontsize=12)
        fig1.tight_layout()
        dietary_conditions_path = f"{folder_path}/dietary_conditions_chart.png"
        fig1.savefig(dietary_conditions_path)
        plt.close(fig1)  # Close the figure after saving

        # Save the time taken bar chart
        fig2, ax2 = plt.subplots(figsize=(5, 3))
        ax2.bar(
            [d["time_taken"] for d in time_data],
            [d["count"] for d in time_data],
            color="lightgreen",
        )
        ax2.set_title("Recipes by Time Taken", fontsize=14)
        ax2.set_xlabel("Time (minutes)", fontsize=12)
        ax2.set_ylabel("Count", fontsize=12)
        fig2.tight_layout()
        time_taken_path = f"{folder_path}/time_taken_chart.png"
        fig2.savefig(time_taken_path)
        plt.close(fig2)

        # Save the dietary conditions pie chart
        fig3, ax3 = plt.subplots(figsize=(5, 3))
        ax3.pie(
            counts,
            labels=dietary_conditions,
            autopct="%1.1f%%",
            startangle=140,
        )
        ax3.set_title("Recipes by Dietary Conditions", fontsize=14)
        fig3.tight_layout()
        pie_chart_path = f"{folder_path}/dietary_conditions_pie_chart.png"
        fig3.savefig(pie_chart_path)
        plt.close(fig3)

        # Notify the user
        tk.messagebox.showinfo("Success", f"Insights saved as images in {folder_path}")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Failed to save insights: {e}")

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('Assets/logo.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Cook-Mate Analytics Report', 0, 0, 'C')
        # Line break
        self.ln(20)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

def generate_analytics_report(user_name=''):
    print("""""""""username.....""""",user_name);
    """
    Generate Cook-Mate Analytics Report and save as a PDF.
    :param user_name: str, the username of the admin generating the report.
    """
    connection = db_config.create_connection()  # Connect to the database
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)

            # Fetch total active users
            cursor.execute("SELECT COUNT(*) AS total_users FROM Users")
            total_active_users = cursor.fetchone()["total_users"]

            # Fetch total recipes
            cursor.execute("SELECT COUNT(*) AS total_recipes FROM Recipes")
            total_recipes = cursor.fetchone()["total_recipes"]

            # Fetch dietary preference distribution
            cursor.execute("""
                SELECT 
                    dietary_preference,
                    COUNT(*) AS user_count,
                    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Users), 2) AS percentage
                FROM Users
                GROUP BY dietary_preference
                ORDER BY user_count DESC
            """)
            dietary_distribution = cursor.fetchall()

            # Fetch user role analysis
            cursor.execute("""
                SELECT 
                    role,
                    COUNT(*) AS count,
                    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Users), 2) AS percentage
                FROM Users
                GROUP BY role
                ORDER BY count DESC
            """)
            role_distribution = cursor.fetchall()

            # Fetch recipe analytics
            cursor.execute("""
                SELECT 
                    dietary_condition,
                    COUNT(*) AS recipe_count,
                    ROUND(AVG(time_taken), 2) AS avg_preparation_time
                FROM Recipes
                GROUP BY dietary_condition
                ORDER BY recipe_count DESC
            """)
            recipe_distribution = cursor.fetchall()

            # Fetch top contributors
            cursor.execute("""
                SELECT 
                    u.name AS user_name, 
                    COUNT(r.recipe_id) AS recipes_created,
                    ROUND(AVG(r.time_taken), 2) AS avg_recipe_time
                FROM Users AS u
                JOIN Recipes AS r ON u.user_id = r.user_id
                GROUP BY u.user_id, u.name
                ORDER BY recipes_created DESC
                LIMIT 10
            """)
            top_contributors = cursor.fetchall()

            # Generate PDF Report
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Report Header
            pdf.set_font("Arial", "B", size=12)
            pdf.cell(200, 10, txt="Cook-Mate Analytics Report", ln=True, align="C")
            #print("generated_________by",user_name)
            generated_by = user_name.strip() if user_name.strip() else "Admin"
            pdf.cell(200, 10, txt=f"Generated By: {generated_by}", ln=True, align="C")
            pdf.cell(200, 10, txt=f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
            pdf.ln(10)

            # Section 1: Executive Summary
            pdf.set_font("Arial", "B", size=12)
            pdf.cell(0, 10, "1. Executive Summary", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, f"Total Active Users: {total_active_users}", ln=True)
            pdf.cell(0, 10, f"Total Recipes: {total_recipes}", ln=True)
            pdf.ln(10)

            # Section 2: Dietary Preference Distribution
            pdf.set_font("Arial", "B", size=12)
            pdf.cell(0, 10, "2. Dietary Preference Distribution", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.cell(80, 10, "Dietary Preference", 1, 0, "C")
            pdf.cell(40, 10, "User Count", 1, 0, "C")
            pdf.cell(40, 10, "Percentage", 1, 1, "C")
            for row in dietary_distribution:
                pdf.cell(80, 10, row['dietary_preference'], 1)
                pdf.cell(40, 10, str(row['user_count']), 1, 0, "C")
                pdf.cell(40, 10, f"{row['percentage']}%", 1, 1, "C")
            pdf.ln(10)

            # Section 3: Recipe Analytics 
            pdf.set_font("Arial", "B", size=12)
            pdf.cell(0, 10, "3. Recipe Analytics", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.cell(80, 10, "Dietary Condition", 1, 0, "C")
            pdf.cell(40, 10, "Recipe Count", 1, 0, "C")
            pdf.cell(40, 10, "Avg Prep Time (mins)", 1, 1, "C")
            for row in recipe_distribution:
                pdf.cell(80, 10, row['dietary_condition'], 1)
                pdf.cell(40, 10, str(row['recipe_count']), 1, 0, "C")
                pdf.cell(40, 10, str(row['avg_preparation_time']), 1, 1, "C")
            pdf.ln(10)

            # Section 4: Top Contributors 
            pdf.set_font("Arial", "B", size=12)
            pdf.cell(0, 10, "4. Top Contributors", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.cell(80, 10, "User Name", 1, 0, "C")
            pdf.cell(40, 10, "Recipes Created", 1, 0, "C")
            pdf.cell(40, 10, "Avg Prep Time (mins)", 1, 1, "C")
            for contributor in top_contributors:
                pdf.cell(80, 10, contributor['user_name'], 1)
                pdf.cell(40, 10, str(contributor['recipes_created']), 1, 0, "C")
                pdf.cell(40, 10, str(contributor['avg_recipe_time']), 1, 1, "C")
            pdf.ln(10)

            # Save PDF
            pdf.output("CookMate_Analytics_Report.pdf")

            messagebox.showinfo("Success", "Cook-Mate Analytics Report generated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {e}")
        finally:
            db_config.close_connection(connection)


            


# def generate_pdf_with_visuals(user_name, insights):
#     """
#     Generate a PDF report including analytics insights and visuals.
#     :param user_name: str, Username of the admin generating the report.
#     :param insights: dict, Data insights for the report.
#     """
#     try:
#         # Initialize PDF
#         pdf = FPDF()
#         pdf.set_auto_page_break(auto=True, margin=15)
#         pdf.add_page()

#         # Add Header
#         pdf.set_font("Arial", "B", 16)
#         pdf.set_text_color(0, 102, 204)
#         pdf.cell(0, 10, "Cook-Mate Analytics Report", ln=True, align="C")

#         # Add "Generated By" and "Generated On"
#         pdf.set_font("Arial", size=12)
#         pdf.set_text_color(0, 0, 0)
#         pdf.cell(0, 10, f"Generated By: {user_name if user_name else 'Admin'}", ln=True, align="C")
#         pdf.cell(0, 10, f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
#         pdf.ln(10)

#         # Add insights content
#         pdf.set_font("Arial", "B", 14)
#         pdf.cell(0, 10, "Analytics Summary:", ln=True)
#         pdf.set_font("Arial", size=12)
#         pdf.cell(0, 10, f"Total Users: {insights.get('total_users', 'N/A')}", ln=True)
#         pdf.cell(0, 10, f"Total Recipes: {insights.get('total_recipes', 'N/A')}", ln=True)
#         pdf.ln(10)

#         # Add dietary conditions analysis
#         pdf.set_font("Arial", "B", 14)
#         pdf.cell(0, 10, "1. Recipes by Dietary Conditions", ln=True)
#         pdf.set_font("Arial", size=12)
#         for condition, count in zip(insights.get('dietary_conditions', []), insights.get('counts', [])):
#             pdf.cell(0, 10, f"{condition}: {count}", ln=True)
#         pdf.ln(10)

#         # Add user dietary preferences analysis
#         pdf.set_font("Arial", "B", 14)
#         pdf.cell(0, 10, "2. Users by Dietary Preferences", ln=True)
#         pdf.set_font("Arial", size=12)
#         for preference, count in zip(insights.get('user_dietary_preferences', []), insights.get('user_diet_counts', [])):
#             pdf.cell(0, 10, f"{preference}: {count}", ln=True)
#         pdf.ln(10)

#         # Add user recipe contributions
#         pdf.set_font("Arial", "B", 14)
#         pdf.cell(0, 10, "3. User Recipe Contributions", ln=True)
#         pdf.set_font("Arial", size=12)
#         for data in insights.get('user_recipe_data', []):
#             pdf.cell(0, 10, f"{data['user_name']}: {data['recipe_count']} recipes", ln=True)
#         pdf.ln(10)

#         # Save the PDF
#         file_path = filedialog.asksaveasfilename(
#             defaultextension=".pdf",
#             filetypes=[("PDF Files", "*.pdf")],
#             title="Save Analytics Report"
#         )
#         if file_path:
#             pdf.output(file_path)
#             messagebox.showinfo("Success", f"Analytics report saved to {file_path}")
#         else:
#             messagebox.showwarning("Cancelled", "Report generation cancelled.")

#     except Exception as e:
#         messagebox.showerror("Error", f"Failed to generate report: {e}")