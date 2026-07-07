# Mosques Management System (Python + Tkinter + SQLite + Folium)

A desktop GUI application for managing a database of mosques, built with Python, Tkinter, and SQLite. It supports adding, searching, updating, and deleting mosque records, plus displaying a mosque's location on an interactive map using Folium.

## Features

- 🗄️ **Persistent storage** using SQLite (`mosques.db`), created automatically on first run.
- ➕ **Add** new mosque records with ID, name, type, address, coordinates, and imam name.
- 🔍 **Search** by name, with **smart suggestions** (using `difflib`) if no exact match is found.
- ✏️ **Update** a mosque's imam name directly from the GUI.
- 🗑️ **Delete** records by ID.
- 📋 **Display all** records in a scrollable list.
- 🖱️ Click a record in the list to auto-fill the input fields for quick editing.
- 🗺️ **Show on Map** — opens an interactive map (via Folium + Leaflet) centered on the selected mosque's coordinates, with a popup marker showing its name.
- ✅ **Input validation** — required fields, numeric ID, and correct `lat,lon` coordinate format are all checked before saving.

## Requirements

```bash
pip install folium
```

`tkinter` and `sqlite3` are part of the Python standard library, so no extra installation is needed for them. An internet connection is required the first time the map is opened, since map tiles are loaded from OpenStreetMap.

## How to Run

```bash
python mosques_management.py
```

## How to Use

1. Fill in the mosque details: **ID**, **Name**, **Type** (Jame / Masjid / Small Mosque), **Address**, **Coordinates** (`lat,lon`), and **Imam Name**.
2. Click **Add Entry** to save a new record.
3. Click **Display All** to list every mosque in the database.
4. Enter a name and click **Search** to find a specific mosque (with suggestions for close matches if not found).
5. Select a record from the list to auto-fill its fields, then:
   - Click **Update Entry** to change its imam name.
   - Click **Delete Entry** to remove it.
   - Click **Display on Map** to view its location in your browser.

## Database Schema

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER (Primary Key) | Unique mosque identifier |
| `name` | TEXT | Mosque name |
| `type` | TEXT | Jame / Masjid / Small Mosque |
| `address` | TEXT | City or area |
| `coordinates` | TEXT | Latitude and longitude, format `lat,lon` |
| `imam_name` | TEXT | Name of the mosque's imam |

## Code Structure

| Component | Purpose |
|---|---|
| `MosqueDB` | Handles all SQLite operations: create table, insert, search, search by ID, delete, update imam, and fetch all names |
| `add_entry()` | Validates input and inserts a new mosque record |
| `search_entry()` | Searches by name; falls back to `difflib` suggestions on no match |
| `delete_entry()` | Deletes a record by ID |
| `update_entry()` | Updates the imam name for a selected mosque |
| `display_all()` | Lists every record in the listbox |
| `fill_fields()` | Auto-fills input fields when a listbox record is selected |
| `validate_inputs()` | Checks required fields, numeric ID, and coordinate format |
| `show_map()` | Generates and opens an interactive Folium map for the selected mosque |

## Possible Future Improvements

- Show all mosques on a single map with multiple markers instead of one at a time.
- Add sorting/filtering by type or address.
- Replace raw `lat,lon` text entry with a map-picker for coordinates.
- Add confirmation dialogs before delete/update actions.
- Export the mosque list to CSV or Excel.

---

## 👩‍💻 Author

**Arwa Alzain**

- 📧 Email: [arwaahalzain@gmail.com](mailto:arwaahalzain@gmail.com)
- 💼 LinkedIn: [linkedin.com/in/arwa-alzain](https://www.linkedin.com/in/arwa-alzain/)
- 🐙 GitHub: [github.com/Arwa-alzain](https://github.com/Arwa-alzain)

---

✨ *Feel free to fork the project, explore the code, and experiment with new features.*
