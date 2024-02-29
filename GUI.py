import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import socket
import subprocess

class WebsiteBlockerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Website Blocker")

        # Create New List button
        self.create_list_button = tk.Button(master, text="Create New List", command=self.create_new_list)
        self.create_list_button.pack(pady=10)

        # Button to select and display content of the selected table
        self.select_table_button = tk.Button(master, text="Select from the List", command=self.display_table_list)
        self.select_table_button.pack(pady=10)

    def display_table_list(self):
        # Create a new window for table selection
        table_selection_window = tk.Toplevel(self.master)
        table_selection_window.title("Select Table")

        # Connect to the database
        conn = sqlite3.connect('website_blocker.db')
        cursor = conn.cursor()

        # Get the list of tables in the database excluding 'sqlite_sequence'
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name!='sqlite_sequence';")
        tables = cursor.fetchall()

        # Create variables to store the checkbox states
        checkbox_vars = []

        # Function to handle blocking from the selected tables
        def block_selected_tables():
            selected_tables = [table[0] for table, var in zip(tables, checkbox_vars) if var.get()]
            if selected_tables:
                # Get the IP addresses from the selected tables
                ip_addresses = self.get_ip_addresses_from_tables(selected_tables)

                # Block incoming traffic from the selected IP addresses
                self.block_ip_addresses(ip_addresses)

                messagebox.showinfo("Block from the Lists", f"Websites blocked from tables: {selected_tables}")
                table_selection_window.destroy()
            else:
                messagebox.showwarning("Select Table", "Please select at least one table.")

        # Create checkboxes for each table
        for table in tables:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(table_selection_window, text=table[0], variable=var)
            checkbox.pack(anchor=tk.W)
            checkbox_vars.append(var)

        # Button to block websites from selected tables
        block_button = tk.Button(table_selection_window, text="BLOCK", command=block_selected_tables)
        block_button.pack(pady=10)

        # Close the connection
        conn.close()

    def get_ip_addresses_from_tables(self, tables):
        # Connect to the database
        conn = sqlite3.connect('website_blocker.db')
        cursor = conn.cursor()

        # Fetch IP addresses from selected tables
        ip_addresses = []
        for table in tables:
            cursor.execute(f"SELECT DISTINCT site_name FROM {table}")
            results = cursor.fetchall()
            ip_addresses.extend([result[0] for result in results])

        # Close the connection
        conn.close()

        return ip_addresses

    def block_ip_addresses(self, ip_addresses):
        try:
            # Ensure that the script is run with sudo privileges
            subprocess.check_call(['sudo', 'echo', 'Running with sudo privileges'])

            # Full path to iptables
            iptables_path = '/usr/sbin/iptables'

            # Block incoming traffic from the specified IP addresses using iptables
            for ip in ip_addresses:
                subprocess.check_call(['sudo', iptables_path, '-A', 'INPUT', '-s', ip, '-j', 'DROP'])

            print(f"Blocked incoming traffic from IP addresses: {ip_addresses}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def create_new_list(self):
        # Ask for the name of the new list
        list_name = simpledialog.askstring("Create New List", "Enter the name of the new list:")
        if list_name:
            self.create_list_table(list_name)

    def create_list_table(self, list_name):
        # Connect to the database
        conn = sqlite3.connect('website_blocker.db')
        cursor = conn.cursor()

        # Create a new table for the list
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {list_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name TEXT NOT NULL
            )
        ''')

        # Commit changes and close the connection
        conn.commit()
        conn.close()

        # Prompt user to add websites to the new list
        self.add_websites_to_list(list_name)

    def add_websites_to_list(self, list_name):
        # Create a new window for input
        input_window = tk.Toplevel(self.master)
        input_window.title("Enter Websites")

        # Text widget for multiple lines input
        input_text = tk.Text(input_window, height=10, width=40)
        input_text.pack(pady=10)

        # Button to submit the input
        submit_button = tk.Button(input_window, text="Submit", command=lambda: self.insert_websites_into_table(list_name, input_text.get("1.0", "end-1c")))
        submit_button.pack(pady=10)

    def insert_websites_into_table(self, list_name, websites_input):
        # Connect to the database
        conn = sqlite3.connect('website_blocker.db')
        cursor = conn.cursor()

        # Split input into a list of websites
        websites_list = [site.strip() for site in websites_input.split('\n') if site.strip()]

        # Convert websites to IP addresses and insert into the table
        for site in websites_list:
            try:
                ip_address = socket.gethostbyname(site)
                cursor.execute(f"INSERT INTO {list_name} (site_name) VALUES (?)", (ip_address,))
            except socket.error as e:
                print(f"Error converting {site} to IP address: {e}")

        # Commit changes and close the connection
        conn.commit()
        conn.close()

        messagebox.showinfo("Website Blocker", f"Websites added to the {list_name} list.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WebsiteBlockerApp(root)
    root.mainloop()

