import sqlite3
import tkinter as tk
from tkinter import messagebox
import webbrowser
import folium
import difflib

class MosqueDB:
    def __init__(self):
        self.conn = sqlite3.connect('mosques.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS mosques (
                id INTEGER PRIMARY KEY,
                name TEXT,
                type TEXT,
                address TEXT,
                coordinates TEXT,
                imam_name  TEXT
            )
        """)
        self.conn.commit()

    def display(self):
        self.cur.execute('SELECT * FROM mosques')
        return self.cur.fetchall()

    def search(self, name):
        self.cur.execute('SELECT * FROM mosques WHERE name=?', (name,))
        return self.cur.fetchone()
    
    def search_by_id(self, id):
        self.cur.execute('SELECT * FROM mosques WHERE id=?', (id,))
        return self.cur.fetchone()

    def insert(self, id, name, type_, address, coordinates, imam_name):
        try:
            self.cur.execute('INSERT INTO mosques VALUES (?, ?, ?, ?, ?, ?)', (id, name, type_, address, coordinates, imam_name))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def delete(self, id):
        self.cur.execute('DELETE FROM mosques WHERE id=?', (id,))
        self.conn.commit()

    # EXTRA: used to retrieve all names for smart suggestions
    def get_all_names(self):
        self.cur.execute('SELECT name FROM mosques')
        return [row[0] for row in self.cur.fetchall()]
    
    # EXTRA: Update Imam Name feature 
    def update_imam(self, mosque_id, new_imam):
        self.cur.execute(
            "UPDATE mosques SET imam_name=? WHERE id=?",
            (new_imam, mosque_id)
        )
        self.conn.commit()

    def __del__(self):
        try:
            self.conn.close()
        except:
            pass
        

db = MosqueDB()

root = tk.Tk()
root.title('Mosques Management System')
root.geometry('800x600')

# input fields
tk.Label(root, text='ID').grid(row=0, column=0, sticky="w", padx=10)
id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1, pady=5)

tk.Label(root, text='Name').grid(row=1, column=0, sticky="w", padx=10)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1, pady=5)

type_var = tk.StringVar(value="Jame")
tk.Label(root, text='Type').grid(row=2, column=0, sticky="w", padx=10)
tk.OptionMenu(root, type_var, "Jame", "Masjid", "Small Mosque").grid(row=2, column=1, pady=5, sticky="w")

tk.Label(root, text='Address').grid(row=3, column=0, sticky="w", padx=10)
address_entry = tk.Entry(root)
address_entry.grid(row=3, column=1, pady=5)

tk.Label(root, text='Coordinates (lat, lon)').grid(row=4, column=0, sticky="w", padx=10)
coordinates_entry = tk.Entry(root)
coordinates_entry.grid(row=4, column=1, pady=5)

tk.Label(root, text='Imam Name').grid(row=5, column=0, sticky="w", padx=10)
imam_entry = tk.Entry(root)
imam_entry.grid(row=5, column=1, pady=5)

# list box
listbox = tk.Listbox(root, width=90)
listbox.grid(row=8, column=0, columnspan=3, pady=10, padx=10)

# functions
def clear_list():
    listbox.delete(0, tk.END)

def display_all():
    clear_list()
    for row in db.display():
        listbox.insert(tk.END, row)

def add_entry():
    if not validate_inputs():
        return
    success = db.insert(
        int(id_entry.get()),
        name_entry.get(),
        type_var.get(),
        address_entry.get(),
        coordinates_entry.get(),
        imam_entry.get()
    )
    if success:
        messagebox.showinfo("Success", "Entry added successfully!")
        display_all()
    else:
        messagebox.showerror("Error", "ID already exists!")

def search_entry():
    clear_list()
    name = name_entry.get()
    if not name:
        messagebox.showerror("Error", "Please enter a name to search!")
        return
        
    result = db.search(name)

    if result:
        listbox.insert(tk.END, result)
    else:
         # EXTRA: Smart search suggestions using difflib
        all_names = db.get_all_names()
        matches = difflib.get_close_matches(name, all_names, n=3)

        if matches:
            listbox.insert(tk.END, "No exact match found. Did you mean: ")
            for m in matches:
                listbox.insert(tk.END, m)
        else:
            listbox.insert(tk.END, "No match found")

def delete_entry():
    if not id_entry.get():
        messagebox.showerror("Error", "Enter ID to delete!")
        return
    db.delete(id_entry.get())
    messagebox.showinfo("Success", "Entry deleted successfully!")
    display_all()

def fill_fields(event):
    selected = listbox.curselection()
    if selected:
        data = listbox.get(selected[0])
        # Only fill fields if the selected item is a valid record (tuple), not a message or suggestion
        if isinstance(data, tuple):
            id_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            address_entry.delete(0, tk.END)
            coordinates_entry.delete(0, tk.END)
            imam_entry.delete(0, tk.END)

            id_entry.insert(tk.END, data[0])
            name_entry.insert(tk.END, data[1])
            type_var.set(data[2])
            address_entry.insert(tk.END, data[3])
            coordinates_entry.insert(tk.END, data[4])
            imam_entry.insert(tk.END, data[5])

listbox.bind("<<ListboxSelect>>", fill_fields)

# EXTRA: Update Imam through GUI
def update_entry():
    if not id_entry.get() or not imam_entry.get():
        messagebox.showerror("Error", "Please select a mosque and enter the new Imam name!")
        return
    db.update_imam(id_entry.get(), imam_entry.get())
    messagebox.showinfo("Success", "Imam updated successfully!")
    display_all()

# EXTRA: Input validation to prevent errors
def validate_inputs():
    if not id_entry.get() or not name_entry.get():
        messagebox.showerror("Error", "ID and Name are required!")
        return False

    try:
        int(id_entry.get())
    except ValueError:
        messagebox.showerror("Error", "ID must be a number!")
        return False

    coords = coordinates_entry.get()
    if coords:
        try:
            lat, lon = coords.split(',')
            float(lat)
            float(lon)
        except ValueError:
            messagebox.showerror("Error", "Coordinates must be in format: lat,lon")
            return False

    return True

# EXTRA: Display mosque location on map using Folium
def show_map():
    selected = listbox.curselection()

    if not selected:
        messagebox.showerror("Error", "Select a mosque from the list to display on map!")
        return
        
    data = listbox.get(selected[0])
    if not isinstance(data, tuple):
        messagebox.showerror("Error", "Please select a valid mosque record!")
        return

    mosque_id = data[0]
    row = db.search_by_id(mosque_id) 
    
    if not row or not row[4]:
        messagebox.showerror("Error", "No coordinates available for this mosque!")
        return
        
    try:
        lat, lon = map(float, row[4].split(','))
    except ValueError:
        messagebox.showerror("Error", "Invalid coordinates format in database! (Expected: lat,lon)")
        return

    m = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Marker([lat, lon], popup=row[1]).add_to(m)
    m.save('map.html')
    webbrowser.open('map.html')

# buttons
tk.Button(root, text='Display All', command=display_all, width=12).grid(row=6, column=0, pady=5)
tk.Button(root, text='Search', command=search_entry, width=12).grid(row=6, column=1, pady=5)
tk.Button(root, text='Add Entry', command=add_entry, width=12).grid(row=6, column=2, pady=5)
tk.Button(root, text='Delete Entry', command=delete_entry, width=12).grid(row=7, column=0, pady=5)
tk.Button(root, text="Update Entry", command=update_entry, width=12).grid(row=7, column=1, pady=5)
tk.Button(root, text="Display on Map", command=show_map, width=12).grid(row=7, column=2, pady=5)

root.mainloop()