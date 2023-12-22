import tkinter as tk
import LOLStats as lol

window = tk.Tk()
window.title("LOL Stats")


# Frame to hold the dynamic form
form_frame = tk.Frame(window)
form_frame.pack(fill="both", expand=True)

# Frame to hold the buttons
tk.Button(window, text="Option 1", command=lambda: create_form(1)).pack(fill='x')
tk.Button(window, text="Option 2", command=lambda: create_form(2)).pack(fill='x')
tk.Button(window, text="Option 3", command=lambda: create_form(3)).pack(fill='x')
tk.Button(window, text="Exit", command=lambda: create_form(4)).pack(fill='x')

# Function to fetch the values from the form
def fetch_values(entries, option):

    # Clear any existing data in the form frame
    for widget in form_frame.winfo_children():
        if isinstance(widget, tk.Label):
            widget.destroy()

    # Extract values from the entries
    values = {entry["label"]: entry["widget"].get() for entry in entries}

    # Check which option was selected
    # Option 1: Get stats for a single champion
    if option == 1:
        if values['Champ'] == '' or values['Role'] == '':
            print("No entries")
            return
        else:
            # Assuming values contain 'Champ' and 'Role'
            champ = values.get("Champ")
            role = values.get("Role")

            # Now call lol.getChampData with the extracted values
            for stats in lol.getChampData(role, champ).items():
                title = stats[0]
                value = stats[1]
                combined = title + ": " + value
                tk.Label(form_frame, text=combined).pack(fill='x')

    # Option 2: Get stats for two champions
    elif option == 2:
        if values['Champ1'] == '' or values['Champ2'] == '' or values['Role'] == '':
            print("No entries")
            return
        else:
            # Assuming values contain 'Champ1', 'Champ2' and 'Role'
            champ1 = values.get("Champ1")
            champ2 = values.get("Champ2")
            role = values.get("Role")

            # Now call lol.getChampData with the extracted values
            for stats in lol.getChampData(role, champ1).items():
                title = stats[0]
                value = stats[1]
                combined = title + ": " + value
                tk.Label(form_frame, text=combined).pack(fill='x')

            for stats in lol.getChampData(role, champ2).items():
                title = stats[0]
                value = stats[1]
                combined = title + ": " + value
                tk.Label(form_frame, text=combined).pack(fill='x')

    else:
        print("Invalid option")

def create_form(option):

    # Clear the current form
    for widget in form_frame.winfo_children():
        widget.destroy()

    entries = []

    # Create a new form based on the option
    if option == 1:
        champ_entry = tk.Entry(form_frame)
        role_entry = tk.Entry(form_frame)
        # Example for Option 1
        tk.Label(form_frame, text="Champ:").pack(fill='x')
        champ_entry.pack()
        tk.Label(form_frame, text="Role:").pack(fill='x')
        role_entry.pack()
        tk.Button(form_frame, text="Submit", command=lambda: fetch_values(entries, option)).pack(fill='x')

        entries.append({"label": "Champ", "widget": champ_entry})
        entries.append({"label": "Role", "widget": role_entry})

    elif option == 2:
        champ1_entry = tk.Entry(form_frame)
        champ2_entry = tk.Entry(form_frame)
        role_entry = tk.Entry(form_frame)
        # Example for Option 2
        tk.Label(form_frame, text="Champ 1:").pack(fill='x')
        champ1_entry.pack()
        tk.Label(form_frame, text="Champ 2:").pack(fill='x')
        champ2_entry.pack()
        tk.Label(form_frame, text="Role:").pack(fill='x')
        role_entry.pack()
        tk.Button(form_frame, text="Submit", command=lambda: fetch_values(entries, option)).pack(fill='x')

        entries.append({"label": "Champ1", "widget": champ1_entry})
        entries.append({"label": "Champ2", "widget": champ2_entry})
        entries.append({"label": "Role", "widget": role_entry})

    elif option == 3:
        tk.Label(form_frame, text="All Champs here").pack(fill='x')
        for champ in lol.GetAllChampList():
            tk.Label(form_frame, text=champ).pack(fill='x')

    elif option == 4:
        tk.Label(form_frame, text="GoodBye").pack(fill='x')
        exit()

window.mainloop()
