import os
import random
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image, ImageTk
from prettytable import PrettyTable


#Database Connection
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Divya7Bhosale",
        database="udaan"
    )
    cursor = connection.cursor(buffered=True)
except Exception as db_err:
    connection = None
    cursor = None
    print(f"Warning: Could not connect to MySQL database: {db_err}")

#App Theme (Hex Codes & Font)
THEME_BG = "#177387"
THEME_FG = "#1a1a1a"
light = "#d1eaf0"

#To get icon images from asset folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def load_icon(name, size=(120, 120)):
    for folder in [BASE_DIR, os.path.join(BASE_DIR, "assets")]:
        full_path = os.path.join(folder, name)
        if os.path.exists(full_path):
            return ImageTk.PhotoImage(Image.open(full_path).resize(size))
    raise FileNotFoundError(f"Icon '{name}' not found in {BASE_DIR} or assets folder.")


class Application:
    def __init__(self, root):
        self.root = root
        self.table = ""
        self.fields = []
        self.entries = {}
        self.entries2 = {}
        self.check_vars = {}

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Admin Dashboard")
        self.root.geometry("800x450")
        self.root.resizable(False, False)
        self.root.update_idletasks()
        self.root.geometry(
            f"+{(self.root.winfo_screenwidth() - 800) // 2}"
            f"+{(self.root.winfo_screenheight() - 450) // 2}"
        )
        self.root.configure(bg=THEME_BG)

        #Preload all icons
        self.admn = load_icon("admn.png")
        self.employe = load_icon("employe.png")
        self.passengr = load_icon("passengr.png")
        self.flight = load_icon("flight.png")
        self.tickt = load_icon("tickt.png")

        self.add_img = load_icon("add.png")
        self.display_img = load_icon("display.png")
        self.update_img = load_icon("update.png")
        self.delete_img = load_icon("delete.png")

        #Main app frame
        self.frame1 = tk.Frame(self.root, bg=light, relief="groove", bd=2)
        self.frame1.place(x=20, y=20, width=760, height=410)

        self.show_table_selection()



#================== TABLE SELECTION ==================
    def show_table_selection(self):
        self.table = ""
        for widget in self.frame1.winfo_children():
            widget.destroy()

        #Title and subtitle
        tk.Label(
            self.frame1,
            text="Flight & Passenger Management",
            fg="#177387",
            font=("Lucida Max", 24),
            bg=light
        ).place(x=140, y=40, width=480, height=40)

        tk.Label(
            self.frame1,
            text="Select a table below to view or modify records",
            fg="#177387",
            font=("Lucida Max", 15),
            bg=light
        ).place(x=160, y=120, width=420, height=30)

        #Table selection buttons
        tables = [
            ("Admin", self.admn, 40),
            ("Employees", self.employe, 180),
            ("Passengers", self.passengr, 320),
            ("Flights", self.flight, 460),
            ("Tickets", self.tickt, 600),
        ]

        for tbl_name, icon, x_pos in tables:
            tk.Button(
                self.frame1,
                image=icon,
                command=lambda t=tbl_name: self.select_table(t),
                bg=light,
                borderwidth=0,
                cursor="hand2"
            ).place(x=x_pos, y=205, width=120, height=120)

            tk.Label(
                self.frame1,
                text=tbl_name,
                fg="#0d3f4a",
                font=("Lucida Max", 12),
                bg=light
            ).place(x=x_pos, y=330, width=120, height=30)

    def select_table(self, table_name):
        self.table = table_name
        self.admin_func()



#================== ADMIN FUNCTIONS ==================
    def admin_func(self):
        for widget in self.frame1.winfo_children():
            widget.destroy()

        #Back button so you can return to table selection
        back = tk.Button(
            self.frame1,
            text="Back",
            bg="#177387",
            fg="white",
            command=self.show_table_selection,
            font=("Lucida Max", 10),
            cursor="hand2"
        )
        back.place(x=664, y=378, width=120, height=35)

        #Title and subtitle
        tk.Label(
            self.frame1,
            text="Flight & Passenger Management",
            fg="#177387",
            font=("Lucida Max", 24),
            bg=light
        ).place(x=140, y=40, width=480, height=40)

        tk.Label(
            self.frame1,
            text="Select which function to perform",
            fg="#177387",
            font=("Lucida Max", 15),
            bg=light
        ).place(x=160, y=120, width=420, height=30)

        #Operation buttons
        operations = [
            ("Add", self.add_img, self.open_add, 60),
            ("Display", self.display_img, self.open_disp, 230),
            ("Update", self.update_img, self.open_update, 410),
            ("Delete", self.delete_img, self.open_delete, 580),
        ]

        for op_name, icon, cmd, x_pos in operations:
            tk.Button(
                self.frame1,
                image=icon,
                command=cmd,
                bg=light,
                borderwidth=0,
                cursor="hand2"
            ).place(x=x_pos, y=205, width=120, height=120)

            tk.Label(
                self.frame1,
                text=op_name,
                fg="#0d3f4a",
                font=("Lucida Max", 12),
                bg=light
            ).place(x=x_pos, y=330, width=120, height=30)

    def get_table_fields(self):
        if not cursor:
            messagebox.showerror("Database Error", "No active database connection.")
            return []
        cursor.execute(f"DESCRIBE {self.table}")
        return [row[0] for row in cursor.fetchall()]

    def open_add(self):
        self.fields = self.get_table_fields()
        if self.fields:
            self.add_func(self.fields)

    def open_disp(self):
        self.fields = self.get_table_fields()
        if self.fields:
            self.disp_func(self.fields)

    def open_update(self):
        self.fields = self.get_table_fields()
        if self.fields:
            self.update_func(self.fields)

    def open_delete(self):
        self.fields = self.get_table_fields()
        if self.fields:
            self.delete_func(self.fields)



#================== ADD RECORD ==================
    def add_func(self, fields):
        for widget in self.frame1.winfo_children():
            widget.destroy()

        back = tk.Button(
            self.frame1,
            text="Back",
            bg="#177387",
            fg="white",
            command=self.admin_func,
            font=("Lucida Max", 10),
            cursor="hand2"
        )
        back.place(x=664, y=378, width=120, height=35)

        self.entries = {}
        for i, field_name in enumerate(fields):
            y_pos = 80 + (i * 40)
            tk.Label(self.frame1, text=f"{field_name}:", font=("Lucida Max", 11), bg="#a2ddeb"
                     ).place(x=150, y=y_pos, width=150, height=25)
            ent = tk.Entry(self.frame1, font=("Arial", 11))
            ent.place(x=310, y=y_pos, width=250, height=25)
            self.entries[field_name] = ent

        tk.Button(
            self.frame1,
            text="Save Record",
            bg="#177387",
            fg="white",
            command=self.add_record,
            font=("Lucida Max", 11),
            cursor="hand2"
        ).place(x=310, y=80 + (len(fields) * 40) + 15, width=120, height=35)

    def add_record(self):
        if not cursor:
            messagebox.showerror("Database Error", "No active database connection.")
            return
        raw_vals = [self.entries[f].get() for f in self.fields]
        vals = tuple(int(x) if x.isdigit() else x for x in raw_vals)
        try:
            placeholders = ", ".join(["%s"] * len(vals))
            cursor.execute(f"INSERT INTO {self.table} VALUES ({placeholders})", vals)
            connection.commit()
            messagebox.showinfo("Success", "Record saved successfully!")
            self.admin_func()
        except Exception as e:
            messagebox.showerror("Error", str(e))



#================== DISPLAY RECORDS ==================
    def disp_func(self, fields):
        for widget in self.frame1.winfo_children():
            widget.destroy()

        back = tk.Button(
            self.frame1,
            text="Back",
            bg="#177387",
            fg="white",
            command=self.admin_func,
            font=("Lucida Max", 10),
            cursor="hand2"
        )
        back.place(x=664, y=378, width=120, height=35)

        tk.Label(
            self.frame1,
            text=f"{self.table} Records",
            font=("Lucida Max", 18, "bold"),
            bg=light,
            fg="#177387"
        ).place(x=220, y=15, width=320, height=35)

        self.check_vars = {}
        for i, field_name in enumerate(fields):
            var = tk.IntVar(value=1)
            self.check_vars[field_name] = var
            tk.Checkbutton(self.frame1, text=field_name, variable=var, bg="#a2ddeb", font=("Lucida Max", 11)
                           ).place(x=150, y=80 + (i * 30))

        tk.Button(
            self.frame1,
            text="Select",
            bg="#177387",
            fg="white",
            command=self.disp_table,
            font=("Lucida Max", 11),
            cursor="hand2"
        ).place(x=310, y=80 + (len(fields) * 30), width=120, height=35)

    def disp_table(self):
        if not cursor:
            messagebox.showerror("Database Error", "No active database connection.")
            return
        cols = [i for i, var in self.check_vars.items() if var.get() == 1]
        if not cols:
            messagebox.showwarning("Warning", "Please select at least one column.")
            return
        d_table = PrettyTable()
        d_table.field_names = cols
        try:
            cursor.execute(f"SELECT {', '.join(cols)} FROM {self.table}")
            for row in cursor.fetchall():
                d_table.add_row(row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        for widget in self.frame1.winfo_children():
            widget.destroy()

        back = tk.Button(
            self.frame1,
            text="Back",
            bg="#177387",
            fg="white",
            command=lambda: self.disp_func(self.fields),
            font=("Lucida Max", 10),
            cursor="hand2"
        )
        back.place(x=664, y=378, width=120, height=35)

        tk.Label(
            self.frame1,
            text=f"{self.table} Records",
            font=("Lucida Max", 18, "bold"),
            bg=light,
            fg="#177387"
        ).place(x=220, y=15, width=320, height=35)

        tk.Label(
            self.frame1,
            text=str(d_table),
            font=("Courier New", 10),
            bg=light,
            fg="#0d3f4a",
            anchor="center",
            bd=1,
            padx=10,
            pady=10
        ).place(x=20, y=60, width=720, height=330)
        back.lift()



#================== UPDATE RECORD ==================
    def update_func(self, fields):
        for widget in self.frame1.winfo_children():
            widget.destroy()

        back = tk.Button(
            self.frame1,
            text="Back",
            bg="#177387",
            fg="white",
            command=self.admin_func,
            font=("Lucida Max", 10),
            cursor="hand2"
        )
        back.place(x=664, y=378, width=120, height=35)

        tk.Label(self.frame1, text=f"{fields[0]}:", font=("Lucida Max", 11), bg="#a2ddeb"
                 ).place(x=230, y=177, width=100, height=28)

        uid_entry = tk.Entry(self.frame1, font=("Arial", 11))
        uid_entry.place(x=340, y=177, width=150, height=28)

        tk.Button(
            self.frame1,
            text="Next",
            bg="#177387",
            fg="white",
            command=lambda: self.on_next(fields, uid_entry),
            font=("Lucida Max", 11),
            cursor="hand2"
        ).place(x=332, y=260, width=96, height=32)

    def on_next(self, fields, uid_entry):
        if not cursor:
            messagebox.showerror("Database Error", "No active database connection.")
            return
        uid = uid_entry.get().strip()
        if not uid:
            messagebox.showwarning("Warning", f"Please enter {fields[0]}.")
            return
        try:
            cursor.execute(f"SELECT * FROM {self.table} WHERE {fields[0]} = %s", (uid,))
            record = cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        if record is None:
            messagebox.showerror("Not Found", f"No record found with {fields[0]} = {uid}")
            return

        for widget in self.frame1.winfo_children():
            widget.destroy()

        back = tk.Button(
            self.frame1,
            text="Back",
            bg="#177387",
            fg="white",
            command=lambda: self.update_func(fields),
            font=("Lucida Max", 10),
            cursor="hand2"
        )
        back.place(x=664, y=378, width=120, height=35)

        self.entries2 = {}
        for i, field_name in enumerate(fields):
            y_pos = 60 + (i * 35)
            tk.Label(self.frame1, text=f"{field_name}:", font=("Lucida Max", 11), bg="#a2ddeb"
                     ).place(x=150, y=y_pos, width=150, height=25)
            ent = tk.Entry(self.frame1, font=("Arial", 11))
            ent.insert(0, str(record[i]))
            ent.place(x=310, y=y_pos, width=250, height=25)
            self.entries2[field_name] = ent

        tk.Button(
            self.frame1,
            text="Update Record",
            bg="#177387",
            fg="white",
            command=self.update_record,
            font=("Lucida Max", 11),
            cursor="hand2"
        ).place(x=310, y=60 + (len(fields) * 35), width=120, height=35)

    def update_record(self):
        if not cursor:
            messagebox.showerror("Database Error", "No active database connection.")
            return
        col = list(self.entries2.keys())
        set_clause = ", ".join([f"{c} = %s" for c in col])
        val = [self.entries2[c].get() for c in col] + [self.entries2[col[0]].get()]
        try:
            cursor.execute(f"UPDATE {self.table} SET {set_clause} WHERE {col[0]} = %s", tuple(val))
            connection.commit()
            messagebox.showinfo("Success", "Record updated successfully!")
            self.admin_func()
        except Exception as e:
            messagebox.showerror("Error", str(e))



#================== DELETE RECORD ==================
    def delete_func(self, fields):
        for widget in self.frame1.winfo_children():
            widget.destroy()

        back = tk.Button(
            self.frame1,
            text="Back",
            bg="#177387",
            fg="white",
            command=self.admin_func,
            font=("Lucida Max", 10),
            cursor="hand2"
        )
        back.place(x=664, y=378, width=120, height=35)

        tk.Label(self.frame1, text=f"{fields[0]}:", font=("Lucida Max", 11), bg="#a2ddeb"
                 ).place(x=230, y=177, width=100, height=28)

        uid_entry = tk.Entry(self.frame1, font=("Arial", 11))
        uid_entry.place(x=340, y=177, width=150, height=28)

        tk.Button(
            self.frame1,
            text="Delete",
            bg="#177387",
            fg="white",
            command=lambda: self.dele(uid_entry, fields),
            font=("Lucida Max", 11),
            cursor="hand2"
        ).place(x=332, y=260, width=96, height=32)

    def dele(self, uid_entry, fields):
        if not cursor:
            messagebox.showerror("Database Error", "No active database connection.")
            return
        uid = uid_entry.get().strip()
        if not uid:
            messagebox.showwarning("Warning", f"Please enter {fields[0]}.")
            return
        try:
            #Check if the record exists
            cursor.execute(f"SELECT * FROM {self.table} WHERE {fields[0]} = %s", (uid,))
            if cursor.fetchone() is None:
                messagebox.showerror("Not Found", f"No record found with {fields[0]} = {uid}")
                return
            cursor.execute(f"DELETE FROM {self.table} WHERE {fields[0]} = %s", (uid,))
            connection.commit()
            messagebox.showinfo("Success", "Record deleted successfully!")
            self.admin_func()
        except Exception as e:
            messagebox.showerror("Error", str(e))


class Application2:
    def __init__(self, root, passenger_id):
        self.root = root
        self.pid  = passenger_id

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Passenger Dashboard")
        self.root.geometry("800x450")
        self.root.resizable(False, False)
        self.root.update_idletasks()
        self.root.geometry(
            f"+{(self.root.winfo_screenwidth() - 800) // 2}"
            f"+{(self.root.winfo_screenheight() - 450) // 2}"
        )
        self.root.configure(bg=THEME_BG)

        #Preload all icons
        self.bookf = load_icon("bookf.png", size=(70, 70))
        self.view = load_icon("ticket.png", size=(90, 70))
        self.status = load_icon("status.png",size=(70, 70))
        self.avflights = load_icon("avflights.png", size=(70, 60))
        self.cancel = load_icon("cancel.png", size=(90, 70))
        self.pasd = load_icon("passengr.png", size=(70, 70))

        self.frame1 = tk.Frame(self.root, bg=light, relief="groove", bd=2)
        self.frame1.place(x=20, y=20, width=760, height=410)

        self.__show_menu()



#================== PASSENGER MENU ==================
    def __show_menu(self):
        for widget in self.frame1.winfo_children():
            widget.destroy()

        self.label1 = tk.Label(self.frame1, text="Udaan Airlines - Passenger Portal", fg="#177387", font=("Lucida Max", 24), bg=light)
        self.label1.place(x=130, y=40, width=520, height=40)
        self.label2 = tk.Label(self.frame1, text="Select a service below to manage your travel", fg="#177387", font=("Lucida Max", 15), bg=light)
        self.label2.place(x=190, y=90, width=420, height=30)

        self.button6 = tk.Button(self.frame1, image=self.bookf, text=" Book Flight", compound="left", fg="#0d3f4a", font=("Lucida Max", 12), bg=light, command=self.on_button6, bd=0, anchor="w", justify="left")
        self.button6.place(x=40, y=160, width=190, height=70)

        self.button7 = tk.Button(self.frame1, image=self.view, text=" View Boarding\n Pass", compound="left", fg="#0d3f4a", font=("Lucida Max", 12), bg=light, command=self.on_button7, bd=0, anchor="w", justify="left")
        self.button7.place(x=285, y=160, width=210, height=70)

        self.button8 = tk.Button(self.frame1, image=self.status, text=" Check Flight\n Status", compound="left", fg="#0d3f4a", font=("Lucida Max", 12), bg=light, command=self.on_button8, bd=0, anchor="w", justify="left")
        self.button8.place(x=530, y=160, width=190, height=70)

        self.button9 = tk.Button(self.frame1, image=self.avflights, text=" View Available\n Flights", compound="left", fg="#0d3f4a", font=("Lucida Max", 12), bg=light, command=self.on_button9, bd=0, anchor="w", justify="left")
        self.button9.place(x=40, y=290, width=190, height=70)

        self.button10 = tk.Button(self.frame1, image=self.cancel, text=" Cancel Flight", compound="left", fg="#0d3f4a", font=("Lucida Max", 12), bg=light, command=self.on_button10, bd=0, anchor="w", justify="left")
        self.button10.place(x=285, y=290, width=190, height=70)

        self.button11 = tk.Button(self.frame1, image=self.pasd, text=" Modify Passenger\n Details", compound="left", fg="#0d3f4a", font=("Lucida Max", 12), bg=light, command=self.on_button11, bd=0, anchor="w", justify="left")
        self.button11.place(x=530, y=290, width=210, height=70)

    def p_update(self):
        col = list(self.entries2.keys())
        set_clause = ", ".join([f"{i} = %s" for i in col])
        val = [ent.get() for ent in self.entries2.values()] + [self.entries2[col[0]].get()]
        cursor.execute(f"UPDATE Passengers SET {set_clause} WHERE {col[0]} = %s", tuple(val))
        connection.commit()
        self.__show_menu()



#================== BOOK FLIGHT ==================
    def on_button6(self):
        for widget in self.frame1.winfo_children():
            widget.destroy()

        tk.Label(self.frame1, text="Book Flight", font=("Lucida Max", 18, "bold"), bg=light, fg="#177387").place(x=230, y=30, width=300, height=35)

        cursor.execute("SELECT FlightID, Airline, Departure, Arrival, DD, DT, Gate FROM Flights")
        flights = cursor.fetchall()
        flight_options = {f"{f[0]} | {f[2]} → {f[3]}": f for f in flights}
        rprice = {f[0]: random.randint(10, 150) for f in flights}

        tk.Label(self.frame1, text="Select Flight:", font=("Lucida Max", 11, "bold"), bg=light, fg="#177387", anchor="w").place(x=110, y=85, width=120, height=28)
        selected_flight = tk.StringVar()
        flight_dd = ttk.Combobox(self.frame1, textvariable=selected_flight, values=list(flight_options.keys()), state="readonly", font=("Arial", 11))
        flight_dd.place(x=245, y=85, width=400, height=28)

        flight_detail = tk.Label(self.frame1, text="", font=("Courier New", 9, "bold"), bg=light, fg="#177387", bd=1, anchor="center")
        flight_detail.place(x=40, y=130, width=680, height=85)

        tk.Label(self.frame1, text="Cabin Class:", font=("Lucida Max", 11, "bold"), bg=light, fg="#177387", anchor="w").place(x=110, y=240, width=130, height=28)
        selected_class = tk.StringVar(value="Economy")
        class_cb = ttk.Combobox(self.frame1, textvariable=selected_class, values=["Economy", "Business", "First Class"], state="readonly", font=("Arial", 11))
        class_cb.place(x=245, y=240, width=180, height=28)

        tk.Label(self.frame1, text="Enter Seat:", font=("Lucida Max", 11, "bold"), bg=light, fg="#177387", anchor="w").place(x=110, y=280, width=130, height=28)
        vcmd = (self.root.register(lambda text: len(text) <= 3), "%P")
        seat_entry = tk.Entry(self.frame1, font=("Arial", 11), validate="key", validatecommand=vcmd)
        seat_entry.place(x=245, y=280, width=180, height=28)

        def on_flight_change(event=None):
            if not selected_flight.get():
                return
            fid, airline, dep, arr, dd, dt, gate = flight_options[selected_flight.get()]
            pt = PrettyTable()
            pt.field_names = ["Flight ID", "Airline", "From", "To", "Date", "Time", "Gate", "Price"]
            pt.add_row([fid, airline, dep, arr, dd, dt, gate, rprice[fid]])
            flight_detail.config(text=str(pt))

        flight_dd.bind("<<ComboboxSelected>>", on_flight_change)
        if flight_options:
            flight_dd.current(0)
            on_flight_change()

        def confirm_booking():
            fid     = flight_options[selected_flight.get()][0]
            price   = rprice[fid]
            seat    = seat_entry.get().strip().upper()
            class_e = selected_class.get()
            if not seat:
                messagebox.showwarning("Missing Info", "Please enter a seat (e.g., 12A).")
                return
            cursor.execute("SELECT 1 FROM Tickets WHERE FlightID = %s AND Seat = %s", (fid, seat))
            if cursor.fetchone():
                messagebox.showerror("Seat Taken", f"Seat {seat} is already booked. Please choose another seat.")
                return
            while True:
                tid = random.randint(1000, 9999)
                cursor.execute("SELECT 1 FROM Tickets WHERE TicketID = %s", (tid,))
                if not cursor.fetchone():
                    break
            cursor.execute("DELETE FROM Tickets WHERE PassengerID = %s", (self.pid,))
            cursor.execute(
                "INSERT INTO Tickets (TicketID, PassengerID, FlightID, Seat, Class, Price) VALUES (%s, %s, %s, %s, %s, %s)",
                (tid, self.pid, fid, seat, class_e, int(price) * 100)
            )
            connection.commit()
            self.__show_menu()

        tk.Button(self.frame1, text="Confirm Booking", bg="#177387", fg="white", font=("Lucida Max", 11), command=confirm_booking).place(x=245, y=340, width=180, height=38)
        back = tk.Button(self.frame1, text="Back", bg="#177387", fg="white", command=self.__show_menu)
        back.place(x=664, y=378, width=120, height=35)
        back.lift()



#================== VIEW BOARDING PASS ==================
    def on_button7(self):
        cursor.execute("SELECT 1 FROM Tickets WHERE PassengerID = %s", (self.pid,))
        if cursor.fetchone() is None:
            messagebox.showwarning("No Ticket Found", "You need to book a flight first!")
            return
        for widget in self.frame1.winfo_children():
            widget.destroy()

        back = tk.Button(self.frame1, text="Back", bg="#177387", fg="white", command=self.__show_menu)
        back.place(x=664, y=378, width=120, height=35)

        #Fetching ticket, passenger and flight data
        cursor.execute("SELECT FlightID, Seat, Class FROM Tickets WHERE PassengerID = %s", (self.pid,))
        row1 = cursor.fetchone()
        FID, Seat, Class = row1

        cursor.execute("SELECT FirstName, LastName FROM Passengers WHERE PID = %s", (self.pid,))
        Name = " ".join(cursor.fetchone())

        cursor.execute("SELECT Airline, Departure, Arrival, DT, DD, Gate FROM Flights WHERE FlightID = %s", (FID,))
        Airline, Dep, Arr, DT, DD, Gate = cursor.fetchone()

        #Boarding pass background
        self.bp = load_icon("bp.png", size=(720, 300))
        self.label8 = tk.Label(self.frame1, image=self.bp, bg=light)
        self.label8.place(relx=0.5, rely=0.5, width=720, height=300, anchor="center")

        #Overlay labels on the boarding pass image
        self.Airlinelbl = tk.Label(self.frame1, text=(Airline).upper()+" AIRLINES", fg="#FFFFFF", bg="#177387", font=("Cascadia Mono", 18), anchor="w")
        self.Airlinelbl.place(x=135, y=70, width=200, height=30)
        self.Classlbl = tk.Label(self.frame1, text=(Class).upper(), fg="#FFFFFF", bg="#177387", font=("Cascadia Mono", 18), anchor="w")
        self.Classlbl.place(x=540, y=70, width=180, height=30)
        self.Namelbl = tk.Label(self.frame1, text=(Name).upper(), bg="#FFFFFF", font=("Cascadia Mono", 11), anchor="w")
        self.Namelbl.place(x=240, y=140, width=200, height=30)
        self.Namelbl2 = tk.Label(self.frame1, text=(Name).upper(), bg="#FFFFFF", font=("Cascadia Mono", 9), anchor="w")
        self.Namelbl2.place(x=590, y=133, width=140, height=30)
        self.Deplbl = tk.Label(self.frame1, text=(Dep).upper(), bg="#FFFFFF", font=("Cascadia Mono", 11), anchor="w")
        self.Deplbl.place(x=240, y=172, width=130, height=30)
        self.Arrlbl = tk.Label(self.frame1, text=(Arr).upper(), bg="#FFFFFF", font=("Cascadia Mono", 11), anchor="w")
        self.Arrlbl.place(x=240, y=205, width=130, height=30)
        self.FIDlbl = tk.Label(self.frame1, text=(FID).upper(), bg="#FFFFFF", font=("Cascadia Mono", 11), anchor="w")
        self.FIDlbl.place(x=450, y=172, width=90, height=30)
        self.FIDlbl2 = tk.Label(self.frame1, text=(FID).upper(), bg="#FFFFFF", font=("Cascadia Mono", 9), anchor="w")
        self.FIDlbl2.place(x=610, y=159, width=90, height=30)
        self.Datelbl = tk.Label(self.frame1, text=(DD).upper(), bg="#FFFFFF", font=("Cascadia Mono", 11), anchor="w")
        self.Datelbl.place(x=450, y=205, width=90, height=30)
        self.Datelbl2 = tk.Label(self.frame1, text=(DD).upper(), bg="#FFFFFF", font=("Cascadia Mono", 9), anchor="w")
        self.Datelbl2.place(x=587, y=185, width=90, height=30)
        self.Gatelbl = tk.Label(self.frame1, text=(Gate).upper(), bg="#FFFFFF", font=("Cascadia Mono", 20), anchor="w")
        self.Gatelbl.place(x=115, y=270, width=200, height=30)
        self.Gatelbl2 = tk.Label(self.frame1, text=(Gate).upper(), bg="#FFFFFF", font=("Cascadia Mono", 9), anchor="w")
        self.Gatelbl2.place(x=587, y=210, width=90, height=30)
        self.Timelbl = tk.Label(self.frame1, text=(DT).upper(), bg="#FFFFFF", font=("Cascadia Mono", 20), anchor="w")
        self.Timelbl.place(x=222, y=270, width=200, height=30)
        self.Seatlbl = tk.Label(self.frame1, text=(Seat).upper(), bg="#FFFFFF", font=("Cascadia Mono", 20), anchor="w")
        self.Seatlbl.place(x=372, y=270, width=70, height=30)
        self.Seatlbl2 = tk.Label(self.frame1, text=(Seat).upper(), bg="#FFFFFF", font=("Cascadia Mono", 9), anchor="w")
        self.Seatlbl2.place(x=587, y=236, width=90, height=30)

        back.lift()



#================== CHECK FLIGHT STATUS ==================
    def on_button8(self):
        cursor.execute("SELECT 1 FROM Tickets WHERE PassengerID = %s", (self.pid,))
        if cursor.fetchone() is None:
            messagebox.showwarning("No Ticket Found", "You need to book a flight first!")
            return
        cursor.execute("SELECT FlightID FROM Tickets WHERE PassengerID = %s", (self.pid,))
        FID = cursor.fetchone()

        cursor.execute("DESCRIBE Flights")
        fields = [row[0] for row in cursor.fetchall()]
        d_table = PrettyTable()
        d_table.field_names = fields
        cursor.execute("SELECT * FROM Flights WHERE FlightID = %s", FID)
        for i in cursor.fetchall():
            d_table.add_row(i)

        for widget in self.frame1.winfo_children():
            widget.destroy()

        back = tk.Button(self.frame1, text="Back", bg="#177387", fg="white", command=self.__show_menu)
        back.place(x=664, y=378, width=120, height=35)
        tk.Label(self.frame1, text="Flight Status", font=("Lucida Max", 18, "bold"), bg=light, fg="#177387").place(x=220, y=15, width=320, height=35)
        tk.Label(self.frame1, text=str(d_table), font=("Courier New", 10), bg=light, fg="#0d3f4a", anchor="center", bd=1, padx=10, pady=10).place(relx=0.5, rely=0.5, anchor="center", width=800, height=250)
        back.lift()



#================== VIEW AVAILABLE FLIGHTS ==================
    def on_button9(self):
        cursor.execute("DESCRIBE Flights")
        fields = [row[0] for row in cursor.fetchall()]
        d_table = PrettyTable()
        d_table.field_names = fields
        cursor.execute("SELECT * FROM Flights")
        for i in cursor.fetchall():
            d_table.add_row(i)

        for widget in self.frame1.winfo_children():
            widget.destroy()

        back = tk.Button(self.frame1, text="Back", bg="#177387", fg="white", command=self.__show_menu)
        back.place(x=664, y=378, width=120, height=35)
        tk.Label(self.frame1, text="Available Flights", font=("Lucida Max", 18, "bold"), bg=light, fg="#177387").place(x=220, y=15, width=320, height=35)
        tk.Label(self.frame1, text=str(d_table), font=("Courier New", 10), bg=light, fg="#0d3f4a", anchor="center", bd=1, padx=10, pady=10).place(relx=0.5, rely=0.5, anchor="center", width=800, height=280)
        back.lift()



#================== CANCEL FLIGHT ==================
    def on_button10(self):
        cursor.execute("SELECT 1 FROM Tickets WHERE PassengerID = %s", (self.pid,))
        if cursor.fetchone() is None:
            messagebox.showwarning("No Ticket Found", "You need to book a flight first!")
            return
        cursor.execute("DELETE FROM Tickets WHERE PassengerID = %s", (self.pid,))
        connection.commit()
        messagebox.showinfo("Cancellation", "Ticket Cancelled!")
        self.__show_menu()



#================== MODIFY PASSENGER DETAILS ==================
    def on_button11(self):
        for widget in self.frame1.winfo_children():
            widget.destroy()

        cursor.execute("DESCRIBE Passengers")
        fields = [row[0] for row in cursor.fetchall()]
        cursor.execute(f"SELECT * FROM Passengers WHERE {fields[0]} = %s", (self.pid,))
        record = cursor.fetchone()

        self.entries2 = {}
        for i, field_name in enumerate(fields):
            ent = tk.Entry(self.frame1, font=("Arial", 11))
            ent.insert(0, str(record[i]))
            ent.place(x=310, y=35 + (i * 35), width=250, height=25)
            lbl = tk.Label(self.frame1, text=f"{field_name}:", font=("Lucida Max", 11, "bold"), fg="#177387", bg=light)
            lbl.place(x=150, y=35 + (i * 35), width=150, height=25)
            self.entries2[field_name] = ent

        back = tk.Button(self.frame1, text="Back", bg="#177387", fg="white", command=self.__show_menu)
        back.place(x=664, y=378, width=120, height=35)
        tk.Button(self.frame1, text="Update Details", bg="#177387", fg="white", command=self.p_update, font=("Lucida Max", 11)
                  ).place(x=310, y=40 + (len(fields) * 35), width=120, height=35)



#================== ADMIN DASHBOARD ==================
def admin_dashboard():
    dashboard_root = tk.Tk()
    app = Application(dashboard_root)
    dashboard_root.mainloop()



#================== PASSENGER DASHBOARD ==================
def passenger_dashboard(passenger_id):
    p_root = tk.Tk()
    app = Application2(p_root, passenger_id)
    p_root.mainloop()



#================== LOGIN FUNCTION ==================
def login():
    ID = ID_entry.get().strip()
    password = password_entry.get().strip()

    if not ID or not password:
        messagebox.showwarning("Warning", "Please enter both User ID and Password.")
        return

    #Admin credentials
    if ID == "10047" and password == "Divya7Bhosale":
        messagebox.showinfo("Login Successful", "Welcome, Divya!")
        loginw.destroy()
        admin_dashboard()
    elif ID == "1393" and password == "Hridya@":
        messagebox.showinfo("Login Successful", "Welcome, Hridya!")
        loginw.destroy()
        admin_dashboard()
    elif cursor:
        try:
            #Checking passengers table if user is a passenger
            cursor.execute(
                "SELECT PID, FirstName, LastName FROM Passengers WHERE PID = %s AND password = %s",
                (ID, password)
            )
            row = cursor.fetchone()
            if row:
                pid, first, last = row
                messagebox.showinfo("Login Successful", f"Welcome, {first} {last}!")
                loginw.destroy()
                passenger_dashboard(pid)
            else:
                messagebox.showerror("Login Failed", "Invalid user ID or password.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Login Failed", "Invalid user ID or password.")



#================== MAIN APP RUN ==================
if __name__ == "__main__":
    loginw = tk.Tk()
    loginw.title("Login")
    loginw.geometry("350x250")
    loginw.resizable(False, False)
    loginw.configure(bg=THEME_BG)

    loginw.update_idletasks()
    loginw.geometry(
        f"+{(loginw.winfo_screenwidth() - 350) // 2}"
        f"+{(loginw.winfo_screenheight() - 250) // 2}"
    )

    frame = tk.Frame(loginw, bg=light, padx=35, pady=30, relief="groove", bd=1)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = tk.Label(frame, text="Sign In", font=("Lucida Fax", 16, "bold"), bg=light, fg=THEME_FG)
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

    tk.Label(frame, text="User ID:", font=("Lucida Fax", 10), bg=light).grid(row=1, column=0, sticky="w", pady=5)
    ID_entry = tk.Entry(frame, font=("Arial", 10), width=22)
    ID_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
    ID_entry.focus()

    tk.Label(frame, text="Password:", font=("Lucida Fax", 10), bg=light).grid(row=2, column=0, sticky="w", pady=5)
    password_entry = tk.Entry(frame, font=("Arial", 10), width=22, show="*")
    password_entry.grid(row=2, column=1, pady=5, padx=(10, 0))

    login_button = tk.Button(frame, text="Login", font=("Lucida Fax", 10, "bold"), bg=THEME_BG, fg="white", width=20, cursor="hand2", command=login)
    login_button.grid(row=3, column=0, columnspan=2, pady=(15, 0))

    loginw.bind("<Return>", lambda event: login())
    loginw.mainloop()
