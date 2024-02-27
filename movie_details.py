import tkinter as tk
from tkinter import ttk
import sqlite3

def create_table():
    conn = sqlite3.connect('movie_detail.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS movie (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    genre TEXT NOT NULL,
                    language TEXT NOT NULL,
                    show_time TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

def add_movie():
    name = name_entry.get()
    genre = genre_combobox.get()
    language = language_combobox.get()
    show_time = show_time_combobox.get()
    conn = sqlite3.connect('movie_detail.db')
    c = conn.cursor()
    c.execute("INSERT INTO movie (name, genre, language, show_time) VALUES (?, ?, ?, ?)", (name, genre, language, show_time))
    conn.commit()
    conn.close()
    clear_entries()
    show_movies()

def clear_entries():
    name_entry.delete(0, tk.END)
    genre_combobox.set("")
    language_combobox.set("")
    show_time_combobox.set("")

def show_movies():
    if movies_tree is not None:
        conn = sqlite3.connect('movie_detail.db')
        c = conn.cursor()
        c.execute("SELECT * FROM movie")
        rows = c.fetchall()
        conn.close()

        for row in movies_tree.get_children():
            movies_tree.delete(row)

        for row in rows:
            movies_tree.insert('', tk.END, values=row)

def delete_movie():
    item = movies_tree.focus()
    selected_movie_id = movies_tree.item(item, "values")[0]
    conn = sqlite3.connect('movie_detail.db')
    c = conn.cursor()
    c.execute("DELETE FROM movie WHERE id=?", (selected_movie_id,))
    conn.commit()
    conn.close()
    show_movies()

def edit_movie():
    item = movies_tree.focus()
    if not item:
        return  # No item selected to edit
    selected_movie_id = movies_tree.item(item, "values")[0]
    conn = sqlite3.connect('movie_detail.db')
    c = conn.cursor()
    c.execute("SELECT * FROM movie WHERE id=?", (selected_movie_id,))
    movie_data = c.fetchone()
    conn.close()

    if movie_data:
        edit_window = tk.Toplevel()
        edit_window.title("Edit Movie Details")

        data_frame = tk.LabelFrame(edit_window, text="Edit Movie Details")
        data_frame.pack(padx=10, pady=10)

        tk.Label(data_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry_edit = tk.Entry(data_frame)
        name_entry_edit.insert(0, movie_data[1])
        name_entry_edit.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(data_frame, text="Genre:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        genre_combobox_edit = ttk.Combobox(data_frame, values=["Action", "Comedy", "Drama", "Thriller", "Horror"])
        genre_combobox_edit.insert(0, movie_data[2])
        genre_combobox_edit.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(data_frame, text="Language:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        language_combobox_edit = ttk.Combobox(data_frame, values=["Hindi", "English", "Nepali"])
        language_combobox_edit.insert(0, movie_data[3])
        language_combobox_edit.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(data_frame, text="Show Time:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        show_time_combobox_edit = ttk.Combobox(data_frame, values=["10:00 AM", "1:00 PM", "4:00 PM", "7:00 PM", "10:00 PM"])
        show_time_combobox_edit.insert(0, movie_data[4])
        show_time_combobox_edit.grid(row=3, column=1, padx=5, pady=5)

        def save_changes():
            new_name = name_entry_edit.get()
            new_genre = genre_combobox_edit.get()
            new_language = language_combobox_edit.get()
            new_show_time = show_time_combobox_edit.get()
            conn = sqlite3.connect('movie_detail.db')
            c = conn.cursor()
            c.execute("UPDATE movie SET name=?, genre=?, language=?, show_time=? WHERE id=?", (new_name, new_genre, new_language, new_show_time, selected_movie_id))
            conn.commit()
            conn.close()
            edit_window.destroy()
            show_movies()

        save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
        save_button.pack(pady=5)

def backk():
    root.destroy()  
    import Home_page
    
def main():
    global root, name_entry, genre_combobox, language_combobox, show_time_combobox, movies_tree

    create_table()

    root = tk.Tk()
    root.title("Movie Details Management")

    data_entry_frame = tk.LabelFrame(root, text="Enter Movie Detail")
    data_entry_frame.pack(padx=10, pady=10)

    tk.Label(data_entry_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    name_entry = tk.Entry(data_entry_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(data_entry_frame, text="Genre:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    genre_combobox = ttk.Combobox(data_entry_frame, values=["Action", "Comedy", "Drama", "Thriller", "Horror"])
    genre_combobox.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(data_entry_frame, text="Language:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    language_combobox = ttk.Combobox(data_entry_frame, values=["Hindi", "English", "Nepali"])
    language_combobox.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(data_entry_frame, text="Show Time:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    show_time_combobox = ttk.Combobox(data_entry_frame, values=["10:00 AM", "1:00 PM", "4:00 PM", "7:00 PM", "10:00 PM"])
    show_time_combobox.grid(row=3, column=1, padx=5, pady=5)

    add_button = tk.Button(data_entry_frame, text="Add Movie", command=add_movie)
    add_button.grid(row=4, columnspan=2, padx=5, pady=5)

    display_frame = tk.LabelFrame(root, text="Movie Details")
    display_frame.pack(padx=10, pady=10)

    movies_tree = ttk.Treeview(display_frame, columns=("ID", "Name", "Genre", "Language", "Show Time"), show="headings")
    movies_tree.heading("ID", text="ID")
    movies_tree.heading("Name", text="Name")
    movies_tree.heading("Genre", text="Genre")
    movies_tree.heading("Language", text="Language")
    movies_tree.heading("Show Time", text="Show Time")
    movies_tree.pack()

    edit_button = tk.Button(root, text="Edit Selected", command=edit_movie)
    edit_button.pack(pady=5)

    delete_button = tk.Button(root, text="Delete Selected", command=delete_movie)
    delete_button.pack(pady=5)

    back = tk.Button(root, text="Back", command=backk)
    back.pack(pady=5) 

    show_movies()

    root.mainloop()

if __name__ == "__main__":
    main()

