import csv
import tkinter as tk
from tkinter import ttk, messagebox
import main  # Importing functions from Main.py
from tkinter import Canvas, Scrollbar


# Declare the comboboxes, entry widgets, and other global variables
global app_path_combobox, app_title_combobox, orientation_combobox, base_face_width_entry, browser_arg_entry, username_entry, username_combobox

CSV_PATH = "./user_settings.csv"
sequence = []

def add_to_sequence():
    current_setting = {
        "app_path": app_path_combobox.get(),
        "app_title": app_title_combobox.get(),
        "orientation": orientation_mapping[orientation_combobox.get()],  # Map the human-readable name to pixel information
        "base_face_width": base_face_width_entry.get(),
        "browser_arg": browser_arg_entry.get()
    }
    sequence.append(current_setting)
    messagebox.showinfo("Success", "Settings added to the sequence!")

    # Add the setting to the timeline listbox in a human-readable format
    timeline_listbox.insert(tk.END, f"App: {current_setting['app_title']}, Orientation: {orientation_combobox.get()}")
    
def edit_selected_sequence():
    index = timeline_listbox.curselection()
    if not index:  # No item selected
        messagebox.showerror("Error", "Please select a sequence to edit!")
        return
    
    # Get the current setting from the sequence using the index
    current_setting = sequence[index[0]]
    
    # Fill the input fields with this setting's data
    app_path_combobox.set(current_setting['app_path'])
    app_title_combobox.set(current_setting['app_title'])
    orientation_combobox.set([k for k, v in orientation_mapping.items() if v == current_setting['orientation']][0])  # Get key by value
    base_face_width_entry.delete(0, tk.END)
    base_face_width_entry.insert(0, current_setting['base_face_width'])
    browser_arg_entry.delete(0, tk.END)
    browser_arg_entry.insert(0, current_setting['browser_arg'])
    
    # Remove the current setting from the sequence and listbox
    del sequence[index[0]]
    timeline_listbox.delete(index[0])

def delete_selected_sequence():
    index = timeline_listbox.curselection()
    if not index:  # No item selected
        messagebox.showerror("Error", "Please select a sequence to delete!")
        return

    # Remove the current setting from the sequence and listbox
    del sequence[index[0]]
    timeline_listbox.delete(index[0])

def save_data():
    username = username_entry.get()
    with open(CSV_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        for setting in sequence:
            writer.writerow([
                username, 
                setting["app_path"], 
                setting["app_title"], 
                setting["orientation"], 
                setting["base_face_width"], 
                setting["browser_arg"]
            ])
    messagebox.showinfo("Success", "Sequence saved successfully!")

def apply_settings():
    username = username_combobox.get()  # We are using a combobox to get saved profiles
    settings_list = []
    with open(CSV_PATH, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username:
                settings = {
                    "app_path": row[1],
                    "app_title": row[2],
                    "orientation": row[3],
                    "base_face_width": int(row[4]),  # Convert base_face_width to integer
                    "browser_arg": row[5]
                }
                settings_list.append(settings)
    
    for settings in settings_list:
        width, height, x, y = map(int, settings['orientation'].split(","))
        args = None
        if "Brave" in settings['app_title']:
            args = ["--new-window", settings['browser_arg']]
        main.open_and_resize(settings['app_path'], settings['app_title'], width, height, x, y, args)
        main.capture_and_zoom(base_face_width=settings['base_face_width'])  # Pass the base_face_width


# Function to get all saved usernames from the CSV file
def get_all_usernames():
    usernames = set()
    try:
        with open(CSV_PATH, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                usernames.add(row[0])
    except FileNotFoundError:
        pass
    return list(usernames)

# Add this function to handle the button click:
def handle_register_base_face_width():
    width = main.register_base_face_width()
    if width:
        base_face_width_entry.delete(0, tk.END)
        base_face_width_entry.insert(0, str(width))
        messagebox.showinfo("Success", f"Registered base face width as {width} pixels!")
    else:
        messagebox.showerror("Error", "Failed to detect a face. Please try again!")


# Create the main window
root = tk.Tk()
root.title("User Settings")

# Set minimum window size
root.minsize(500, 400)

# Default settings extracted from the commented section
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

app_paths = [
    "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe",
    "C:/Users/Rugved Chavan/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Visual Studio Code/Visual Studio Code.lnk",
    "Path3"
]

app_titles = ["Brave", "Visual Studio Code", "Other_App2"]

# Create a dictionary for the orientations with human-readable names
orientation_mapping = {
    "Full Left Half": f"{screen_width//2},{screen_height},0,0",
    "Full Right Half": f"{screen_width//2},{screen_height},{screen_width//2},0",
    "Top Left Quarter": f"{screen_width//2},{screen_height//2},0,0",
    "Top Right Quarter": f"{screen_width//2},{screen_height//2},{screen_width//2},0",
    "Bottom Left Quarter": f"{screen_width//2},{screen_height//2},0,{screen_height//2}",
    "Bottom Right Quarter": f"{screen_width//2},{screen_height//2},{screen_width//2},{screen_height//2}"
}

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def display_saved_profile_ui():
    global username_combobox  # Add this line
    clear_window()

    # Combobox to select saved user profiles
    username_select_label = ttk.Label(root, text="Select User Profile")
    username_select_label.pack(pady=10)
    
    username_combobox = ttk.Combobox(root, values=get_all_usernames())
    username_combobox.pack(pady=10)
    
    # Apply saved settings button
    apply_button = ttk.Button(root, text="Apply", command=apply_settings)
    apply_button.pack(pady=20)
    
    back_button = ttk.Button(root, text="Back", command=display_initial_ui)
    back_button.pack(pady=10)

    delete_button = ttk.Button(root, text="Delete User", command=delete_user)
    delete_button.pack(pady=10)

def delete_user():
    username = username_combobox.get()
    if not username:
        messagebox.showerror("Error", "Please select a user to delete!")
        return

    confirmation = messagebox.askyesno("Delete User", f"Do you want to delete the user {username}?")
    if not confirmation:
        return

    all_rows = []
    with open(CSV_PATH, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != username:
                all_rows.append(row)

    with open(CSV_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(all_rows)
    
    messagebox.showinfo("Deleted", f"Settings for {username} have been deleted!")
    display_saved_profile_ui()


def display_new_profile_ui():
    global app_path_combobox, app_title_combobox, orientation_combobox, base_face_width_entry, browser_arg_entry, username_entry, timeline_listbox
    clear_window()

    MIN_HEIGHT = 1200  # Set the minimum height
    MIN_WIDTH = 700   # Set the minimum width

    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient='vertical', command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack Canvas and Scrollbar with the canvas having a minimum height and width
    canvas.pack(side="left", fill="both", expand=True)
    canvas.config(scrollregion=canvas.bbox("all"), height=MIN_HEIGHT, width=MIN_WIDTH)
    scrollbar.pack(side="right", fill="y")



    username_save_label = ttk.Label(scrollable_frame, text="Username for Saving")
    username_save_label.pack(pady=10)
    
    username_entry = ttk.Entry(scrollable_frame, width=50)  # Increased width
    username_entry.pack(pady=10, padx=40)
    
    app_path_label = ttk.Label(scrollable_frame, text="App Path")
    app_path_label.pack(pady=10)
    
    app_path_combobox = ttk.Combobox(scrollable_frame, values=app_paths, width=50)  # Increased width
    app_path_combobox.pack(pady=10)
    
    app_title_label = ttk.Label(scrollable_frame, text="App Title")
    app_title_label.pack(pady=10)
    
    app_title_combobox = ttk.Combobox(scrollable_frame, values=app_titles, width=50)  # Increased width
    app_title_combobox.pack(pady=10)
    
    orientation_label = ttk.Label(scrollable_frame, text="Orientation")
    orientation_label.pack(pady=10)
    
    orientation_combobox = ttk.Combobox(scrollable_frame, values=list(orientation_mapping.keys()), width=50)  # Increased width
    orientation_combobox.pack(pady=10)

    base_face_width_label = ttk.Label(scrollable_frame, text="Base Face Width")
    base_face_width_label.pack(pady=10)
    register_face_width_button = ttk.Button(scrollable_frame, text="Register Base Face Width", command=handle_register_base_face_width)
    register_face_width_button.pack(pady=10)
    
    base_face_width_entry = ttk.Entry(scrollable_frame, width=50)  # Increased width
    base_face_width_entry.pack(pady=10)
    
    browser_arg_label = ttk.Label(scrollable_frame, text="Browser Argument (URL)")
    browser_arg_label.pack(pady=10)
    
    browser_arg_entry = ttk.Entry(scrollable_frame, width=50)  # Increased width
    browser_arg_entry.pack(pady=10)

     # Sequence timeline listbox
    timeline_label = ttk.Label(scrollable_frame, text="Current Sequence Timeline:")
    timeline_label.pack(pady=10)

    timeline_listbox = tk.Listbox(scrollable_frame, width=60, height=10)
    timeline_listbox.pack(pady=10, padx=40)

    edit_sequence_button = ttk.Button(scrollable_frame, text="Edit Selected Sequence", command=edit_selected_sequence)
    edit_sequence_button.pack(pady=5)

    delete_sequence_button = ttk.Button(scrollable_frame, text="Delete Selected Sequence", command=delete_selected_sequence)
    delete_sequence_button.pack(pady=5)
    
    # Save sequence button
    save_button = ttk.Button(scrollable_frame, text="Save", command=save_data)
    save_button.pack(pady=20)

    # Add to Sequence Button
    add_to_sequence_button = ttk.Button(scrollable_frame, text="Add to Sequence", command=add_to_sequence)
    add_to_sequence_button.pack(pady=10)
    
    back_button = ttk.Button(scrollable_frame, text="Back", command=display_initial_ui)
    back_button.pack(pady=10)

def display_initial_ui():
    clear_window()
    logo_image = tk.PhotoImage(file="logo.png")  # Adjust the path if needed
    # logo_image = logo_image.zoom(2, 2)  # Double the width and height

    logo_label = ttk.Label(root, background='#2E2E2E')  # Adjust the background color if needed
    logo_label.image = logo_image  # this line retains a reference to the image
    logo_label['image'] = logo_image
    logo_label.pack(pady=(20, 20))

    app_name_label = ttk.Label(root, text="Dynamic Display", font=("Arial", 24), foreground="white", background='red')
    app_name_label.pack(pady=(15, 30))

    new_button = ttk.Button(root, text="New Profile", command=display_new_profile_ui)
    new_button.pack(pady=20, padx=20)

    saved_button = ttk.Button(root, text="Saved Profile", command=display_saved_profile_ui)
    saved_button.pack(pady=20, padx=20)

    author_label = ttk.Label(root, text="Developed by: Rugved Chavan, Esshaan, Parth", font=("Arial", 12), foreground="black")
    author_label.pack(pady=5)

    website_link_label = ttk.Label(root, text="Visit Our Website", font=("Arial", 12), foreground="blue", cursor="hand2")
    website_link_label.bind("<Button-1>", lambda e: webbrowser.open_new("http://yourwebsite.com"))
    website_link_label.pack(pady=5)

display_initial_ui()

# Making UI More Appealing

style = ttk.Style()

# Root window background
root.configure(bg='#F5F5F5')  # Light Gray

# Configure button appearance
style.configure('TButton', 
                font=('Arial', 12), 
                padding=5, 
                background='#E0E0E0',  # Slightly darker gray
                foreground='#333333',  # Dark gray text
                bordercolor='#E0E0E0',  # Same as the button color
                relief='flat')

style.map('TButton', 
          foreground=[('active', '#333333')],    # Text remains dark gray when active (hovered)
          background=[('active', '#D0D0D0')])  # Button turns even darker gray when active

# Configure labels, entries, and comboboxes
style.configure('TLabel', font=('Arial', 12), background='#F5F5F5', foreground='#333333')
style.configure('TEntry', 
                padding=5, 
                relief='flat', 
                font=('Arial', 10), 
                background='#FFFFFF', 
                foreground='#333333', 
                fieldbackground='#FFFFFF', 
                insertcolor='#333333')  # Cursor color

style.configure('TCombobox', 
                padding=5, 
                font=('Arial', 10), 
                background='#FFFFFF', 
                foreground='#333333')
root.mainloop()
