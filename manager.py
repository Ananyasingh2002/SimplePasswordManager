import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk

def add_password():
    name = simpledialog.askstring("Add Password", "Enter a name for the password:")
    password = simpledialog.askstring("Add Password", "Enter the password:")
    if name and password:  # Check if both values are provided
        cursor.execute('INSERT INTO keys (name, password) VALUES (?, ?)', (name, password))
        conn.commit()
        messagebox.showinfo("Success", "Password added successfully!")

def view_passwords():
    cursor.execute('SELECT id, name, password FROM keys')
    rows = cursor.fetchall()
    password_text = "\n".join([f"ID: {row[0]}, Name: {row[1]}, Password: {row[2]}" for row in rows])
    messagebox.showinfo("Passwords", password_text)

def update_password():
    name = simpledialog.askstring("Update Password", "Enter the name for the password:")
    new_password = simpledialog.askstring("Update Password", "Enter the new password:")
    if name and new_password:  # Check if both values are provided
        cursor.execute('SELECT name FROM keys')
        rows = cursor.fetchall()
        if name in [row[0] for row in rows]:
            cursor.execute('UPDATE keys SET password = ? WHERE name = ?', (new_password, name))
            conn.commit()
            messagebox.showinfo("Success", "Password updated successfully!")
        else:
            messagebox.showerror("Error", f"App '{name}' not found. Password not updated.")

def delete_password():
    cursor.execute('SELECT name FROM keys')
    rows = cursor.fetchall()

    if rows:
        password_names = [row[0] for row in rows]
        selected_name = simpledialog.askstring("Delete Password", "Select the app name to delete:\n",
                                                initialvalue="", parent=root)
        if selected_name:
            if selected_name in password_names:
                delete_option = messagebox.askyesno("Delete Password", f"Do you want to delete both the name and password for '{selected_name}'?")
                if delete_option:
                    cursor.execute('DELETE FROM keys WHERE name = ?', (selected_name,))
                    conn.commit()
                    messagebox.showinfo("Success", f"Password for app '{selected_name}' deleted successfully!")
                else:
                    cursor.execute('UPDATE keys SET password = ? WHERE name = ?', ("", selected_name))
                    conn.commit()
                    messagebox.showinfo("Success", f"Password for app '{selected_name}' name deleted successfully!")
            else:
                messagebox.showerror("Error", f"App '{selected_name}' not found. No password deleted.")
    else:
        messagebox.showinfo("No Passwords", "You haven't saved anything yet.")


conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS keys (
        id INTEGER PRIMARY KEY,
        name TEXT,
        password TEXT
    )
''')

root = tk.Tk()
root.title("Password Manager")

root.geometry("400x300")  # Set the initial size of the window

# Create a label frame for the buttons
button_frame = ttk.LabelFrame(root, text="Password Management", padding=10)
button_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Add some padding to the buttons
button_style = ttk.Style()
button_style.configure("TButton", padding=10, relief="flat")

button_add = ttk.Button(button_frame, text="Add Password", command=add_password, style="TButton")
button_add.pack(fill="x", pady=5)

button_view = ttk.Button(button_frame, text="View Passwords", command=view_passwords, style="TButton")
button_view.pack(fill="x", pady=5)

button_update = ttk.Button(button_frame, text="Update Password", command=update_password, style="TButton")
button_update.pack(fill="x", pady=5)

button_delete = ttk.Button(button_frame, text="Delete Password", command=delete_password, style="TButton")
button_delete.pack(fill="x", pady=5)

root.mainloop()

conn.close()
