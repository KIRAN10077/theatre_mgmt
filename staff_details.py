import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

def create_table():
    conn = sqlite3.connect('staff_detail.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS staff (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    staff_type TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

def add_staff():
    name = name_entry.get()
    contact = contact_entry.get()
    staff_type = staff_type_var.get()

    if not (name and contact and staff_type):
        messagebox.showerror("Error", "Please don't leave any fields empty")
        return
    
    if (len(contact)!=10 ):
        messagebox.showerror("Error","Please enter valid credentials.")
        return

    conn = sqlite3.connect('staff_detail.db')
    c = conn.cursor()
    c.execute("INSERT INTO staff (name, contact, staff_type) VALUES (?, ?, ?)", (name, contact, staff_type))
    conn.commit()
    conn.close()
    clear_entries()
    show_staff()

def clear_entries():
    name_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)

def show_staff():
    if staff_tree is not None:
        conn = sqlite3.connect('staff_detail.db')
        c = conn.cursor()
        c.execute("SELECT * FROM staff")
        rows = c.fetchall()
        conn.close()

        # Clear previous data from the treeview which has been modified or deleted
        for row in staff_tree.get_children():
            staff_tree.delete(row)

        # Display data
        for row in rows:
            staff_tree.insert('', tk.END, values=row)

def on_edit(event=None):
    item = staff_tree.focus()
    selected_staff_id = staff_tree.item(item, "values")[0]
    name = staff_tree.item(item, "values")[1]
    contact = staff_tree.item(item, "values")[2]
    staff_type = staff_tree.item(item, "values")[3]

    edit_window = tk.Toplevel()
    edit_window.title("Edit Staff Details")

    data_frame = tk.LabelFrame(edit_window, text="Edit Staff Details")
    data_frame.pack(padx=10, pady=10)

    tk.Label(data_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    name_entry_edit = tk.Entry(data_frame)
    name_entry_edit.insert(0, name)
    name_entry_edit.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(data_frame, text="Contact:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    contact_entry_edit = tk.Entry(data_frame)
    contact_entry_edit.insert(0, contact)
    contact_entry_edit.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(data_frame, text="Staff Type:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    staff_type_entry_edit = ttk.Combobox(data_frame, values=["Full-time", "Part-time"])
    staff_type_entry_edit.set(staff_type)
    staff_type_entry_edit.grid(row=2, column=1, padx=5, pady=5)

    def save_changes():
        new_name = name_entry_edit.get()
        new_contact = contact_entry_edit.get()
        new_staff_type = staff_type_entry_edit.get()

        conn = sqlite3.connect('staff_detail.db')
        c = conn.cursor()
        c.execute("UPDATE staff SET name=?, contact=?, staff_type=? WHERE id=?", (new_name, new_contact, new_staff_type, selected_staff_id))
        conn.commit()
        conn.close()
        edit_window.destroy()
        show_staff()

    save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
    save_button.pack(pady=5)

def delete_staff():
    item = staff_tree.focus()
    selected_staff_id = staff_tree.item(item, "values")[0]

    conn = sqlite3.connect('staff_detail.db')
    c = conn.cursor()
    c.execute("DELETE FROM staff WHERE id=?", (selected_staff_id,))
    conn.commit()
    conn.close()
    show_staff()

def backk():
    root.destroy()  
    import Home_page

def main():
    global root, name_entry, contact_entry, staff_tree, staff_type_var

    create_table()

    root = tk.Tk()
    root.title("Staff Details Management")

    # Data Entry UI
    data_entry_frame = tk.LabelFrame(root, text="Enter Staff Detail")
    data_entry_frame.pack(padx=10, pady=10)

    tk.Label(data_entry_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    name_entry = tk.Entry(data_entry_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(data_entry_frame, text="Contact:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    contact_entry = tk.Entry(data_entry_frame)
    contact_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(data_entry_frame, text="Staff Type:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    staff_type_var = tk.StringVar()
    staff_type_entry = ttk.Combobox(data_entry_frame, textvariable=staff_type_var, values=["Full-time", "Part-time"])
    staff_type_entry.grid(row=2, column=1, padx=5, pady=5)

    add_button = tk.Button(data_entry_frame, text="Add Staff", command=add_staff)
    add_button.grid(row=3, columnspan=2, padx=5, pady=5)

    # Display Staff Details
    display_frame = tk.LabelFrame(root, text="Staff Details")
    display_frame.pack(padx=10, pady=10)

    staff_tree = ttk.Treeview(display_frame, columns=("ID", "Name", "Contact", "Staff Type"), show="headings")
    staff_tree.heading("ID", text="ID")
    staff_tree.heading("Name", text="Name")
    staff_tree.heading("Contact", text="Contact")
    staff_tree.heading("Staff Type", text="Staff Type")
    staff_tree.pack()

    staff_tree.bind("<Double-1>", on_edit)

    edit_button = tk.Button(root, text="Edit Selected", command=on_edit)
    edit_button.pack(pady=5)

    delete_button = tk.Button(root, text="Delete Selected", command=delete_staff)
    delete_button.pack(pady=5)

    back = tk.Button(root, text="Back", command=backk)
    back.pack(pady=5)  


    show_staff()

    root.mainloop()

if __name__ == "__main__":
    main()
