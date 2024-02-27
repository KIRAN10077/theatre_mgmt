import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

def create_table():
    conn = sqlite3.connect('item_detail.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS item (
                    id INTEGER PRIMARY KEY,
                    item TEXT NOT NULL,
                    category TEXT NOT NULL,
                    rate TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

def add_item():
    item = item_entry.get()
    category = category_combobox.get()
    rate = rate_entry.get()

    if not (item and category and rate):
        messagebox.showerror("Error", "Please don't leave any fields empty")
        return
    
    conn = sqlite3.connect('item_detail.db')
    c = conn.cursor()
    c.execute("INSERT INTO item (item, category, rate) VALUES (?, ?, ?)", (item, category, rate))
    conn.commit()
    conn.close()
    clear_entries()
    show_items()

def clear_entries():
    item_entry.delete(0, tk.END)
    category_combobox.set("")
    rate_entry.delete(0, tk.END)

def show_items():
    if items_tree is not None:
        conn = sqlite3.connect('item_detail.db')
        c = conn.cursor()
        c.execute("SELECT * FROM item")
        rows = c.fetchall()
        conn.close()

        for row in items_tree.get_children():
            items_tree.delete(row)

        for row in rows:
            items_tree.insert('', tk.END, values=row)

def delete_item():
    item = items_tree.focus()
    selected_item_id = items_tree.item(item, "values")[0]
    conn = sqlite3.connect('item_detail.db')
    c = conn.cursor()
    c.execute("DELETE FROM item WHERE id=?", (selected_item_id,))
    conn.commit()
    conn.close()
    show_items()

def edit_item():
    item = items_tree.focus()
    if not item:
        return  # No item selected to edit
    selected_item_id = items_tree.item(item, "values")[0]
    conn = sqlite3.connect('item_detail.db')
    c = conn.cursor()
    c.execute("SELECT * FROM item WHERE id=?", (selected_item_id,))
    item_data = c.fetchone()
    conn.close()

    if item_data:
        edit_window = tk.Toplevel()
        edit_window.title("Edit Item Details")

        data_frame = tk.LabelFrame(edit_window, text="Edit Item Details")
        data_frame.pack(padx=10, pady=10)

        tk.Label(data_frame, text="Item:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        item_entry_edit = tk.Entry(data_frame)
        item_entry_edit.insert(0, item_data[1])
        item_entry_edit.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(data_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        category_combobox_edit = ttk.Combobox(data_frame, values=["Beverages", "Meals"])
        category_combobox_edit.insert(0, item_data[2])
        category_combobox_edit.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(data_frame, text="Rate:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        rate_entry_edit = tk.Entry(data_frame)
        rate_entry_edit.insert(0, item_data[3])
        rate_entry_edit.grid(row=2, column=1, padx=5, pady=5)

        def save_changes():
            new_item = item_entry_edit.get()
            new_category = category_combobox_edit.get()
            new_rate = rate_entry_edit.get()
            conn = sqlite3.connect('item_detail.db')
            c = conn.cursor()
            c.execute("UPDATE item SET item=?, category=?, rate=? WHERE id=?", (new_item, new_category, new_rate, selected_item_id))
            conn.commit()
            conn.close()
            edit_window.destroy()
            show_items()

        save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
        save_button.pack(pady=5)

def backk():
    root.destroy()  
    import Home_page

def main():
    global root, item_entry, category_combobox, rate_entry, items_tree

    create_table()

    root = tk.Tk()
    root.title("Item Details Management")

    menu_label = tk.Label(root, text="MENU", font=("Arial", 80, "bold"))
    menu_label.pack(pady=10)

    display_frame = tk.LabelFrame(root, text="Item Details")
    display_frame.pack(padx=10, pady=10)

    items_tree = ttk.Treeview(display_frame, columns=("ID", "Item", "Category", "Rate"), show="headings")
    items_tree.heading("ID", text="ID")
    items_tree.heading("Item", text="Item")
    items_tree.heading("Category", text="Category")
    items_tree.heading("Rate", text="Rate")
    items_tree.pack()

    edit_button = tk.Button(root, text="Edit Selected", command=edit_item)
    edit_button.pack(pady=5)

    delete_button = tk.Button(root, text="Delete Selected", command=delete_item)
    delete_button.pack(pady=5)

    show_items()
    
    data_entry_frame = tk.LabelFrame(root, text="Enter Item Detail")
    data_entry_frame.pack(padx=10, pady=10)

    tk.Label(data_entry_frame, text="Item:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    item_entry = tk.Entry(data_entry_frame)
    item_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(data_entry_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    category_combobox = ttk.Combobox(data_entry_frame, values=["Beverages", "Meals"])
    category_combobox.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(data_entry_frame, text="Rate:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    rate_entry = tk.Entry(data_entry_frame)
    rate_entry.grid(row=2, column=1, padx=5, pady=5)

    add_button = tk.Button(data_entry_frame, text="Add Item", command=add_item)
    add_button.grid(row=3, columnspan=2, padx=5, pady=5)

    back = tk.Button(root, text="Back", command=backk)
    back.pack(pady=5) 

    root.mainloop()

if __name__ == "__main__":
    main()