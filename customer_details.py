import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox



def create_table():
    conn = sqlite3.connect('customer_detail.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS customer (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    seat_booked INTEGER NOT NULL,  
                    contact TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

def add_customer():
    name = name_entry.get()
    seat_booked = seat_booked_entry.get()
    contact_no = contact_entry.get()

    contact = contact_entry.get()
    if ((not seat_booked) or (not name) or (not contact_no) ):
        messagebox.showerror("Error", "Please enter the valid information.")
        return
    else:
        messagebox.showinfo("Success!",f"Customer with {seat_booked} no. of seats booked Successfully!")

    conn = sqlite3.connect('customer_detail.db')
    c = conn.cursor()
    c.execute("SELECT SUM(seat_booked) FROM customer")
    total_booked_seats = c.fetchone()[0]
    conn.close()

    if total_booked_seats is None:
        total_booked_seats = 0

    if total_booked_seats + int(seat_booked) > 20:
        messagebox.showerror("Error", "No seats available at the moment. Sorry for the inconvenience.")
        return

    conn = sqlite3.connect('customer_detail.db')
    c = conn.cursor()
    c.execute("INSERT INTO customer (name, seat_booked, contact) VALUES (?, ?, ?)", (name, seat_booked, contact))
    conn.commit()
    conn.close()
    clear_entries()
    show_customers()
    update_remaining_seats()

def clear_entries():
    name_entry.delete(0, tk.END)
    seat_booked_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)

def show_customers():
    if customers_tree is not None:
        conn = sqlite3.connect('customer_detail.db')
        c = conn.cursor()
        c.execute("SELECT * FROM customer")
        rows = c.fetchall()
        conn.close()

        for row in customers_tree.get_children():
            customers_tree.delete(row)

        for row in rows:
            customers_tree.insert('', tk.END, values=row)

def on_edit(event=None): 
    item = customers_tree.focus()
    if not item:
        return

    selected_customer_id = customers_tree.item(item, "values")[0]
    name = customers_tree.item(item, "values")[1]
    seat_booked = customers_tree.item(item, "values")[2]
    contact = customers_tree.item(item, "values")[3]

    edit_window = tk.Toplevel()
    edit_window.title("Edit Customer Details")

    data_frame = tk.LabelFrame(edit_window, text="Edit Customer Details")
    data_frame.pack(padx=10, pady=10)

    tk.Label(data_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    name_entry_edit = tk.Entry(data_frame)
    name_entry_edit.insert(0, name)
    name_entry_edit.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(data_frame, text="seat_booked:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    seat_booked_entry_edit = tk.Entry(data_frame)
    seat_booked_entry_edit.insert(0, seat_booked)
    seat_booked_entry_edit.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(data_frame, text="Contact:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    contact_entry_edit = tk.Entry(data_frame)
    contact_entry_edit.insert(0, contact)
    contact_entry_edit.grid(row=2, column=1, padx=5, pady=5)

    def save_changes():
        new_name = name_entry_edit.get()
        new_seat_booked = seat_booked_entry_edit.get()
        new_contact = contact_entry_edit.get()
        conn = sqlite3.connect('customer_detail.db')
        c = conn.cursor()
        c.execute("UPDATE customer SET name=?, seat_booked=?, contact=? WHERE id=?", (new_name, new_seat_booked, new_contact, selected_customer_id))
        conn.commit()
        conn.close()
        edit_window.destroy()
        show_customers()
        update_remaining_seats()

    save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
    save_button.pack(pady=5)

def delete_customer(): 
    item = customers_tree.focus()
    if not item:
        return

    selected_customer_id = customers_tree.item(item, "values")[0]
    conn = sqlite3.connect('customer_detail.db')
    c = conn.cursor()
    c.execute("DELETE FROM customer WHERE id=?", (selected_customer_id,))
    conn.commit()
    conn.close()
    show_customers()
    update_remaining_seats()

def update_remaining_seats():
    global remaining_seats_label  # Declare remaining_seats_label as global
    conn = sqlite3.connect('customer_detail.db')
    c = conn.cursor()
    c.execute("SELECT SUM(seat_booked) FROM customer")
    total_booked_seats = c.fetchone()[0]
    conn.close()

    if total_booked_seats is None:
        total_booked_seats = 0

    remaining_seats = 20 - total_booked_seats
    remaining_seats_label.config(text=f"Total seats remaining: {remaining_seats}")


def backk():
    root.destroy()  
    import Home_page
       

def main():
    global root, name_entry, seat_booked_entry, contact_entry, customers_tree, remaining_seats_label

    create_table()

    root = tk.Tk()
    root.title("Customer Details Management")

    data_entry_frame = tk.LabelFrame(root, text="Enter Customer Detail")
    data_entry_frame.pack(padx=10, pady=10)
    
    tk.Label(data_entry_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    name_entry = tk.Entry(data_entry_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(data_entry_frame, text="seat_booked:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    seat_booked_entry = tk.Entry(data_entry_frame)
    seat_booked_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(data_entry_frame, text="Contact:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    contact_entry = tk.Entry(data_entry_frame)
    contact_entry.grid(row=2, column=1, padx=5, pady=5)

    add_button = tk.Button(data_entry_frame, text="Add Customer", bg="green" ,command=add_customer)
    add_button.grid(row=3, columnspan=2, padx=5, pady=5)

    display_frame = tk.LabelFrame(root, text="Customer Details")
    display_frame.pack(padx=10, pady=10)

    customers_tree = ttk.Treeview(display_frame, columns=("ID", "Name", "seat_booked", "Contact"), show="headings")
    customers_tree.heading("ID", text="ID")
    customers_tree.heading("Name", text="Name")
    customers_tree.heading("seat_booked", text="seat_booked")
    customers_tree.heading("Contact", text="Contact")
    customers_tree.pack()

    customers_tree.bind("<Double-1>", on_edit)

    edit_button = tk.Button(root, text="Edit Selected",bg = "yellow", command=on_edit)
    edit_button.pack(pady=5)

    delete_button = tk.Button(root, text="Delete Selected",bg="orange", command=delete_customer)
    delete_button.pack(pady=5)

    remaining_seats_label = tk.Label(root, text="")
    remaining_seats_label.pack(pady=5)

    update_remaining_seats()

    back = tk.Button(root, text="Back", bg="gray70",command=backk)
    back.pack(pady=5)  

    root.mainloop()


if __name__ == "__main__":
    main()