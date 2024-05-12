import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from PIL import Image, ImageTk
import pymysql
from ttkthemes import ThemedStyle
from datetime import datetime, timedelta

# Database
def connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='enscipurcom',
    )
    return conn

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("1920x1080")
        self.setup_login_page()

    def setup_login_page(self): 
        self.root.configure(bg="white") #Background color

        #Frame sa login page
        login_frame = tk.Frame(root, bd=5, relief="sunken", padx=100, pady=100, highlightthickness=5, highlightbackground="darkgreen")
        login_frame.grid(row=0, column=0)

        # Logo or picture
        original_logo = Image.open('logo.png')
        resized_logo = original_logo.resize((200, 200)) #Size
        tk_logo = ImageTk.PhotoImage(resized_logo)
        self.logo_label = tk.Label(login_frame, image=tk_logo)
        self.logo_label.image = tk_logo
        self.logo_label.grid(row=0, column=0, columnspan=2, pady=(0, 0))  #Height

        title_label = tk.Label(login_frame, text="FARM MANAGER", font=("Arial", 16, "bold")) #Title label
        title_label.grid(row=1, column=0, columnspan=2, pady=(10, 10))  #Height

        username_label = tk.Label(login_frame, text="Username:", font =("Arial", 12, "bold")) 
        password_label = tk.Label(login_frame, text="Password:", font =("Arial", 12, "bold"))

        self.username_entry = tk.Entry(login_frame, width=40)
        self.password_entry = tk.Entry(login_frame, width=40, show='●')
        self.login_button = tk.Button(login_frame, text="Login", font=("Arial", 12), command=self.validate_login, bg="darkgreen", fg="white")

        #Location ng mga field at button sa frame gamit grid
        username_label.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="w")  #Height
        self.username_entry.grid(row=2, column=1, padx=10, pady=(0, 5), sticky="ew")

        password_label.grid(row=3, column=0, padx=10, pady=(0, 5), sticky="w")  #Height
        self.password_entry.grid(row=3, column=1, padx=10, pady=(0, 5), sticky="ew")

        self.login_button.grid(row=4, column=1, padx=10, pady=(10, 0), sticky="ew")  #Height

        login_frame.place(relx=0.28, rely=0.05)

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        #Validation kung tama un at pw
        if username == "a" and password == "1":
            messagebox.showinfo("Login Successful", "Welcome, Farm Manager!")
            self.root.destroy()  # Close the login window

            #Execute kung tama
            self.app_instance = HomePage(tk.Tk())
            print("App instance created")  #Lalabas sa terminal kung tama
            self.app_instance.run()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")

class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Rice Track")
        self.root.geometry("1920x1080")
        
        #Database connection
        self.db_connection = connection()
        self.db_cursor = self.db_connection.cursor(pymysql.cursors.DictCursor)
        
        self.style = ThemedStyle(self.root)
        self.style.set_theme("arc")

        #Load background image
        self.background_image = Image.open("header.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas = tk.Canvas(self.root, width=1200, height=213)
        self.canvas.pack(side=tk.TOP, pady=0, ipadx=0, ipady=0, fill=tk.X)

        #Set background image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_photo)
        self.root.configure(bg='white')

        self.sidebar_frame = ttk.Frame(root, padding=(30, 100, 30, 0), style='Sidebar.TFrame')
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.home_button = ttk.Button(self.sidebar_frame, text="Home", command=self.display_home, style='Sidebar.TButton')
        self.home_button.pack(pady=10, ipady=5, fill=tk.X)

        self.info_button = ttk.Button(self.sidebar_frame, text="System Information", command=self.open_systeminfo, style='Sidebar.TButton')
        self.info_button.pack(pady=10, ipady=5, fill=tk.X)

        self.form_button = ttk.Button(self.sidebar_frame, text="Rice Details", command=self.open_ricedetails, style='Sidebar.TButton')
        self.form_button.pack(pady=10, ipady=5, fill=tk.X)

        self.dashboard_button = ttk.Button(self.sidebar_frame, text="Rice Tracker", command=self.open_ricetracker, style='Sidebar.TButton')
        self.dashboard_button.pack(pady=10, ipady=5, fill=tk.X)
        
        self.logout_button = ttk.Button(self.sidebar_frame, text="Logout", command=self.logout, style='Sidebar.TButton')
        self.logout_button.pack(pady=10, ipady=5, fill=tk.X)

        self.content_frame = ttk.Frame(root, padding=(50, 50, 50, 70), style='Content.TFrame')
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.rice = []

        self.root.style = ttk.Style()

        self.root.style.configure('Sidebar.TButton', background='Black', foreground='Black', font=('Arial', 10, 'bold'), borderwidth=0)
        self.root.style.configure('Sidebar.TFrame', background='olive')
        self.root.style.configure('Content.TFrame', background='White')
        self.root.style.configure('Content.TLabel', background='White', borderwidth=0, relief='solid', padding=(5, 5), foreground='Black')
        self.root.style.configure('Content.TButton', background='Black', foreground='darkgreen', font=('Arial', 10, 'bold'), borderwidth=10)
        
        self.display_home()
        
    def logout(self):
        #Confirmation msg be4 logout
        confirm_logout = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        
        if confirm_logout:
            for widget in self.content_frame.winfo_children():
                widget.destroy()
                
            self.root.destroy()
        else:
            pass
        
    def open_systeminfo(self):
        systeminfo_dsplay = SystemInfo(self.content_frame, root)
        systeminfo_dsplay.display_info()
        
    def open_ricedetails(self):
        ricedetails_display = RiceDetails(self.content_frame, self.db_cursor, root)
        ricedetails_display.owned_not()
        
    def open_ricetracker(self):
        #para ma-open yung students records class
        ricetracker_display = RiceTracker(self.content_frame, self.db_cursor, root)
        ricetracker_display.owned_not()
        
    def populate_table(self):
        #Check if the Treeview widget exists
        if not hasattr(self, 'my_tree'):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        #Kuha lahat ng rice sa database
        self.db_cursor.execute("SELECT id, type_of_rice, qty_of_seeds_sacks, date_planted, estimated_date_harvest, harvested_rice_kg, rice_sold_kg, stocks, sales FROM rice")
        rice = self.db_cursor.fetchall()

        #Insert data into the Treeview
        for rice in rice:
            self.tree.insert(parent='', index='end', iid=rice['id'], values=(
                rice['id'],
                rice['type_of_rice'],
                rice['qty_of_seeds_sacks'],
                rice['date_planted'],
                rice['estimated_date_harvest'],
                rice['harvested_rice_kg'],
                rice['rice_sold_kg'],
                rice['stocks'],
                rice['sales']
            ))

    def clear_content_frame(self):

        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def display_home(self):
        self.clear_content_frame()

        #PNG image
        image_path = "home.png"
        original_image = Image.open(image_path)

        #Size
        resized_image = original_image.resize((1000, 300))  #width at height

        photo = ImageTk.PhotoImage(resized_image)

        image_label = ttk.Label(self.content_frame, image=photo)
        image_label.image = photo
        image_label.pack()
        
        #Text sa baba ng image
        info_text = """
        "Supporting Farmers: Harvesting Growth, Yielding Success."
        """
        info_label = ttk.Label(self.content_frame, text=info_text, font=('Arial', 14, 'italic'), style='Content.TLabel', justify = 'center')
        info_label.pack()
        
    def run(self):
        self.root.mainloop()
        
class SystemInfo(HomePage):
    def __init__(self, content_frame, root):
        self.content_frame = content_frame
        self.root = root
       
    def display_info(self):
        self.clear_content_frame()

        image_path = "systeminfo.png"
        original_image = Image.open(image_path)

        #Size
        resized_image = original_image.resize((1000, 300))

        photo = ImageTk.PhotoImage(resized_image)

        image_label = ttk.Label(self.content_frame, image=photo)
        image_label.image = photo 
        image_label.pack()

        #Text sa baba ng image
        info_text = """
        Rice Tracker empowers farmers by providing them with the tools and insights they need to
        enhance efficiency, maximize yields, and ultimately achieve greater profitability in their farming operations.
        """
        info_label = ttk.Label(self.content_frame, text=info_text, font=('times', 12), style='Content.TLabel', justify = 'center')
        info_label.pack()
        
class RiceDetails(HomePage):
    def __init__(self, content_frame, db_cursor, root):
        self.db_connection = connection()
        self.content_frame = content_frame
        self.db_cursor = db_cursor
        self.db_connection = connection()
        self.db_cursor = self.db_connection.cursor(pymysql.cursors.DictCursor)
        self.root = root
        self.form_entries = {} 
        
    def owned_not(self):
        self.clear_content_frame()

        button_frame = ttk.Frame(self.content_frame)
        button_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        owned_button = ttk.Button(button_frame, text="Owned Rice", command=self.display_rice_form, style='Content.TButton')
        owned_button.pack(side=tk.TOP, pady=(0, 10))
        not_button = ttk.Button(button_frame, text="Pagiling ng Iba", command=self.pagiling_ng_iba_form, style='Content.TButton')
        not_button.pack(side=tk.TOP)
        
    def display_rice_form(self):
        self.clear_content_frame()
        
        #Application form 
        canvas = tk.Canvas(self.content_frame)
        
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        #Frame para sa entry fields
        form_frame = ttk.Frame(canvas)

        canvas.create_window((10, 10), window=form_frame, anchor="nw")

        #Display application form
        form_label = ttk.Label(form_frame, text="RICE DETAILS", font=('Arial', 16, 'bold'), style='Content.TLabel')
        form_label.pack(side=tk.TOP, pady=5, ipadx=370, ipady=10, fill=tk.X)
        
        #Entry fields
        form_fields = [
            "Type of Rice", "Quantity of Seeds (in sacks)", "Date Planted"
        ]

        self.form_entries = {}

        for field in form_fields:

            label = ttk.Label(form_frame, text=field, style='Content.TLabel')
            label.pack(side=tk.TOP, pady=5, ipadx=350, ipady=1, fill=tk.X)

            if field == "Type of Rice":
                entry = ttk.Combobox(form_frame, values=["White", "Brown", "Red"], state="readonly")
            elif field == "Date Planted":
                entry = DateEntry(form_frame, width=12, background='darkgreen', foreground='white', borderwidth=2)

            else:
                entry = ttk.Entry(form_frame, width=30)
            entry.pack(fill=tk.X)
            self.form_entries[field] = entry

        # Submit button
        submit_button = ttk.Button(form_frame, text="Add", command=self.submit_rice, style='Content.TButton')
        submit_button.pack(side=tk.LEFT, pady=20, ipadx=100, padx=150   )
        reset_button = ttk.Button(form_frame, text="Reset Form", command=self.reset_form, style='Content.TButton')
        reset_button.pack(side=tk.LEFT, pady=20, ipadx=100)

        form_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        canvas.pack(side="left", fill="both", expand=True)
    
    def submit_rice(self):
        #Kuha data sa entry fields
        rice_data = {
            'type_of_rice': self.form_entries['Type of Rice'].get(),
            'qty_of_seeds_sacks': self.form_entries['Quantity of Seeds (in sacks)'].get(),
            'date_planted': self.format_date(self.form_entries['Date Planted'].get()),
        }
        
        date_planted = datetime.strptime(rice_data['date_planted'], "%Y-%m-%d")
        quantity = int(rice_data['qty_of_seeds_sacks'])
        rice_data['estimated_date_harvest'] = date_planted + timedelta(days=120) # Assuming 120 days for harvest
        rice_data['harvested_rice_kg'] = quantity * 100  # Assuming 100 kg per sack
        rice_data['rice_sold_kg'] = 0  # 0 kasi hindi pa nabebenta
        rice_data['stocks'] = rice_data['harvested_rice_kg'] - rice_data['rice_sold_kg']
        rice_data['sales'] = 0  # 0 kasi wala pa benta
        
        # Calculation para makuha natitirang stock at yung sales
        rice_data['stocks'] = rice_data['harvested_rice_kg'] - rice_data['rice_sold_kg']
        rice_data['price_per_kg'] = 50.00  # presyo ng kada kilo
        rice_data['sales'] = rice_data['rice_sold_kg'] * rice_data['price_per_kg']
        
        # Validate if all required fields are filled
        required_fields = ['type_of_rice', 'qty_of_seeds_sacks', 'date_planted']
        if all(rice_data[field] for field in required_fields):
            # Insert data into the database
            insert_query = """
            INSERT INTO rice 
            (type_of_rice, qty_of_seeds_sacks, date_planted, estimated_date_harvest, harvested_rice_kg, rice_sold_kg, stocks, sales) 
            VALUES (%(type_of_rice)s, %(qty_of_seeds_sacks)s, %(date_planted)s, %(estimated_date_harvest)s, %(harvested_rice_kg)s, %(rice_sold_kg)s, %(stocks)s, %(sales)s)
            """
            try:
                self.db_cursor.execute(insert_query, rice_data)
                self.db_connection.commit()
                messagebox.showinfo("Success", "Application submitted successfully!")

                # Update sa table after ma-insert bagong data
                self.populate_table()

                self.reset_form()
            except Exception as e:
                messagebox.showerror("Database Error", f"Error submitting application: {e}")
        else:
            messagebox.showwarning("Incomplete Form", "Please fill out all fields.")

    def format_date(self, date_str):
        #Convert yung DateEntry format to 'yyyy-mm-dd' format
        try:
            parsed_date = datetime.strptime(date_str, "%m/%d/%y")
            formatted_date = parsed_date.strftime("%Y-%m-%d")
            return formatted_date
        except ValueError:
            return None

    def reset_form(self):
        for entry in self.form_entries.values():
            if isinstance(entry, ttk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, DateEntry):
                entry.set_date(None)
            elif isinstance(entry, ttk.Combobox):
                entry.set("")
        
    def pagiling_ng_iba_form(self):
        self.clear_content_frame()
        
        #Application form 
        canvas = tk.Canvas(self.content_frame)
        
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        #Frame para sa entry fields
        form_frame = ttk.Frame(canvas)

        canvas.create_window((10, 10), window=form_frame, anchor="nw")

        #Display application form
        form_label = ttk.Label(form_frame, text="PAGILING NG IBA", font=('Arial', 16, 'bold'), style='Content.TLabel')
        form_label.pack(side=tk.TOP, pady=5, ipadx=370, ipady=10, fill=tk.X)
        
        #Entry fields
        form_fields = [
            "Quantity of Rice (in kg)", "Date Received"
        ]

        self.form_entries = {}

        for field in form_fields:

            label = ttk.Label(form_frame, text=field, style='Content.TLabel')
            label.pack(side=tk.TOP, pady=5, ipadx=350, ipady=1, fill=tk.X)

            if field == "Date Received":
                entry = DateEntry(form_frame, width=12, background='darkgreen', foreground='white', borderwidth=2)
            else:
                entry = ttk.Entry(form_frame, width=30)
            entry.pack(fill=tk.X)
            self.form_entries[field] = entry

        # Submit button
        submit_button = ttk.Button(form_frame, text="Add", command=self.submit_pagiling, style='Content.TButton')
        submit_button.pack(side=tk.LEFT, pady=20, ipadx=100, padx=150   )
        reset_button = ttk.Button(form_frame, text="Reset Form", command=self.reset_pagiling_form, style='Content.TButton')
        reset_button.pack(side=tk.LEFT, pady=20, ipadx=100)

        form_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        canvas.pack(side="left", fill="both", expand=True)
        
    def submit_pagiling(self):
        #Kuha data sa entry fields
        rice_data = {
            'qty_of_rice_kg': self.form_entries['Quantity of Rice (in kg)'].get(),
            'date_received': self.format_date(self.form_entries['Date Received'].get())
        }
        
        quantity = int(rice_data['qty_of_rice_kg'])
        
        # Calculation para makuha yung sales
        rice_data['sales'] = quantity * 2  # Assuming 100 kg per sack
        
        # Validate if all required fields are filled
        required_fields = ['qty_of_rice_kg', 'date_received']
        if all(rice_data[field] for field in required_fields):
            # Insert data into the database
            insert_query = """
            INSERT INTO pagiling
            (qty_of_rice_kg, date_received, sales) 
            VALUES (%(qty_of_rice_kg)s, %(date_received)s, %(sales)s)
            """
            try:
                self.db_cursor.execute(insert_query, rice_data)
                self.db_connection.commit()
                messagebox.showinfo("Success", "Application submitted successfully!")

                # Update sa table after ma-insert bagong data
                self.populate_table()

                self.reset_form()
            except Exception as e:
                messagebox.showerror("Database Error", f"Error submitting application: {e}")
        else:
            messagebox.showwarning("Incomplete Form", "Please fill out all fields.")
        
    def reset_pagiling_form(self):
        for entry in self.form_entries.values():
            if isinstance(entry, ttk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, DateEntry):
                entry.set_date(None)
        
class RiceTracker(HomePage):
    def __init__(self, content_frame, db_cursor, root):
        self.db_connection = connection()
        self.content_frame = content_frame
        self.db_cursor = db_cursor
        self.db_connection = connection()
        self.db_cursor = self.db_connection.cursor(pymysql.cursors.DictCursor)
        self.root = root
        self.form_entries = {} 
        self.update_rice_details_window = None
        
    def owned_not(self):
        self.clear_content_frame()

        button_frame = ttk.Frame(self.content_frame)
        button_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        owned_button = ttk.Button(button_frame, text="Owned Rice", command=self.ownedrice, style='Content.TButton')
        owned_button.pack(side=tk.TOP, pady=(0, 10))
        not_button = ttk.Button(button_frame, text="Pagiling ng Iba", command=self.pagiling_ng_iba, style='Content.TButton')
        not_button.pack(side=tk.TOP)
        
    def ownedrice(self):
        self.clear_content_frame()

        self.db_cursor.execute("SELECT * FROM rice")
        rice = self.db_cursor.fetchall()
        
        self.clear_content_frame()
        
        title_label = tk.Label(self.content_frame, text="LIST OF ALL RICE", font=("Arial", 12, 'bold'))
        title_label.pack(pady=0)

        columns = ("ID", "Type of Rice", "Quantity of Seeds (in sacks)", "Date Planted", "Estimated Date of Harvest", "Harvested Rice (in kg)", "Rice Sold (in kg)", "Stocks", "Sales")
        
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")

        # center
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.CENTER)

        # column widths
        self.tree.column("ID", width=10)  
        self.tree.column("Type of Rice", width=50)  
        self.tree.column("Quantity of Seeds (in sacks)", width=100)  
        self.tree.column("Date Planted", width=40)
        self.tree.column("Estimated Date of Harvest", width=90)
        self.tree.column("Harvested Rice (in kg)", width=80)
        self.tree.column("Rice Sold (in kg)", width=55)
        self.tree.column("Stocks", width=45)
        self.tree.column("Sales", width=80)
        
        for col in columns:
            self.tree.heading(col, text=col)

        # Insert data into the Treeview
        for rice in rice:
            self.tree.insert(parent='', index='end', iid=rice['id'], values=(
                rice['id'],
                rice['type_of_rice'],
                rice['qty_of_seeds_sacks'],
                rice['date_planted'],
                rice['estimated_date_harvest'],
                rice['harvested_rice_kg'],
                rice['rice_sold_kg'],
                rice['stocks'],
                rice['sales']
            ))
            
        self.tree.pack(fill=tk.BOTH, expand=True, padx=0, pady=10)

        dashboard_frame = ttk.Frame(self.content_frame, padding=(215, 0, 0, 0), style='Content.TFrame')
        dashboard_frame.pack(fill=tk.X)

        # Dashboard buttons
        highsales_button = ttk.Button(dashboard_frame, text="High Sales", command=self.show_highsales_rice, style='Content.TButton')
        highsales_button.pack(side=tk.LEFT, padx=5)

        lowsales_button = ttk.Button(dashboard_frame, text="Low Sales", command=self.show_lowsales_rice, style='Content.TButton')
        lowsales_button.pack(side=tk.LEFT, padx=5)
        
        update_button = ttk.Button(dashboard_frame, text="Update Rice Details", command=self.update_rice_details, style='Content.TButton')
        update_button.pack(side=tk.LEFT, padx=5)

        remove_button = ttk.Button(dashboard_frame, text="Remove", command=self.remove_rice, style='Content.TButton')
        remove_button.pack(side=tk.LEFT, padx=5)
        
    # DISPLAY
    def display_all_rice(self):
        self.clear_content_frame()

        self.db_cursor.execute("SELECT * FROM rice")
        rice = self.db_cursor.fetchall()
        
        self.clear_content_frame()
        
        title_label = tk.Label(self.content_frame, text="LIST OF ALL RICE", font=("Arial", 12, 'bold'))
        title_label.pack(pady=0)

        columns = ("ID", "Type of Rice", "Quantity of Seeds (in sacks)", "Date Planted", "Estimated Date of Harvest", "Harvested Rice (in kg)", "Rice Sold (in kg)", "Stocks", "Sales")
        
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")

        # center
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.CENTER)

        # column widths
        self.tree.column("ID", width=10)  
        self.tree.column("Type of Rice", width=50)  
        self.tree.column("Quantity of Seeds (in sacks)", width=100)  
        self.tree.column("Date Planted", width=40)
        self.tree.column("Estimated Date of Harvest", width=90)
        self.tree.column("Harvested Rice (in kg)", width=80)
        self.tree.column("Rice Sold (in kg)", width=55)
        self.tree.column("Stocks", width=45)
        self.tree.column("Sales", width=80)
        
        for col in columns:
            self.tree.heading(col, text=col)

        # Insert data into the Treeview
        for rice in rice:
            self.tree.insert(parent='', index='end', iid=rice['id'], values=(
                rice['id'],
                rice['type_of_rice'],
                rice['qty_of_seeds_sacks'],
                rice['date_planted'],
                rice['estimated_date_harvest'],
                rice['harvested_rice_kg'],
                rice['rice_sold_kg'],
                rice['stocks'],
                rice['sales']
            ))
            
        self.tree.pack(fill=tk.BOTH, expand=True, padx=0, pady=10)

        dashboard_frame = ttk.Frame(self.content_frame, padding=(215, 0, 0, 0), style='Content.TFrame')
        dashboard_frame.pack(fill=tk.X)

        # Dashboard buttons
        highsales_button = ttk.Button(dashboard_frame, text="High Sales", command=self.show_highsales_rice, style='Content.TButton')
        highsales_button.pack(side=tk.LEFT, padx=5)

        lowsales_button = ttk.Button(dashboard_frame, text="Low Sales", command=self.show_lowsales_rice, style='Content.TButton')
        lowsales_button.pack(side=tk.LEFT, padx=5)
        
        update_button = ttk.Button(dashboard_frame, text="Update Rice Details", command=self.update_rice_details, style='Content.TButton')
        update_button.pack(side=tk.LEFT, padx=5)

        remove_button = ttk.Button(dashboard_frame, text="Remove", command=self.remove_rice, style='Content.TButton')
        remove_button.pack(side=tk.LEFT, padx=5)

    # HIGH SALES
    def show_highsales_rice(self):
        self.db_cursor.execute("SELECT * FROM rice WHERE sales >= 100000.00;")
        rice = self.db_cursor.fetchall()
        
        self.clear_content_frame()
        
        title_label = tk.Label(self.content_frame, text="LIST OF HIGH SALES", font=("Arial", 12, 'bold'))
        title_label.pack(pady=0)
        
        if rice:
            columns = ("ID", "Type of Rice", "Quantity of Seeds (in sacks)", "Date Planted", "Estimated Date of Harvest", "Harvested Rice (in kg)", "Rice Sold (in kg)", "Stocks", "Sales")
            self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")

            # Center column headings
            for col in columns:
                self.tree.heading(col, text=col, anchor=tk.CENTER)

            # column widths
            column_widths = [10, 50, 100, 40, 90, 80, 55, 45, 80]
            for col, width in zip(columns, column_widths):
                self.tree.column(col, width=width)

            # Insert data into the Treeview para sa high sales
            for rice in rice:
                self.tree.insert(parent='', index='end', iid=rice['id'], values=(
                    rice['id'],
                    rice['type_of_rice'],
                    rice['qty_of_seeds_sacks'],
                    rice['date_planted'],
                    rice['estimated_date_harvest'],
                    rice['harvested_rice_kg'],
                    rice['rice_sold_kg'],
                    rice['stocks'],
                    rice['sales']
                ))

                self.tree.pack(fill=tk.BOTH, expand=True, padx=0, pady=10)

        else:
            # Display message kapag walang high sales na nakita
            label = ttk.Label(self.content_frame, text="No high sales.", style='Content.TLabel')
            label.pack(anchor='w') 

        dashboard_frame = ttk.Frame(self.content_frame, padding=(160, 0, 0, 0), style='Content.TFrame')
        dashboard_frame.pack(fill=tk.X)

        # Dashboard buttons
        all_rice_button = ttk.Button(dashboard_frame, text="All Rice", command=self.display_all_rice, style='Content.TButton')
        all_rice_button.pack(side=tk.LEFT, padx=5)

        lowsales_button = ttk.Button(dashboard_frame, text="Low Sales", command=self.show_lowsales_rice, style='Content.TButton')
        lowsales_button.pack(side=tk.LEFT, padx=5)
        
        remove_button = ttk.Button(dashboard_frame, text="Remove ", command=self.remove_rice, style='Content.TButton')
        remove_button.pack(side=tk.LEFT, padx=5)

    # LOW SALES
    def show_lowsales_rice(self):
        self.db_cursor.execute("SELECT * FROM rice WHERE sales <= 99999.00;")
        rice = self.db_cursor.fetchall()
        
        self.clear_content_frame()
        
        title_label = tk.Label(self.content_frame, text="LIST OF LOW SALES", font=("Arial", 12, 'bold'))
        title_label.pack(pady=0)
        
        if rice:
            columns = ("ID", "Type of Rice", "Quantity of Seeds (in sacks)", "Date Planted", "Estimated Date of Harvest", "Harvested Rice (in kg)", "Rice Sold (in kg)", "Stocks", "Sales")
            self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")

            # Center column headings
            for col in columns:
                self.tree.heading(col, text=col, anchor=tk.CENTER)

            # column widths
            column_widths = [10, 50, 100, 40, 90, 80, 55, 45, 80]
            for col, width in zip(columns, column_widths):
                self.tree.column(col, width=width)

            # Insert data into the Treeview para sa low sales
            for rice in rice:
                self.tree.insert(parent='', index='end', iid=rice['id'], values=(
                    rice['id'],
                    rice['type_of_rice'],
                    rice['qty_of_seeds_sacks'],
                    rice['date_planted'],
                    rice['estimated_date_harvest'],
                    rice['harvested_rice_kg'],
                    rice['rice_sold_kg'],
                    rice['stocks'],
                    rice['sales']
                ))
                
                self.tree.pack(fill=tk.BOTH, expand=True, padx=0, pady=10)

        else:
            # Display message kapag walang low sales na nakita
            label = ttk.Label(self.content_frame, text="No low sales.", style='Content.TLabel')
            label.pack(anchor='w') 
            
        dashboard_frame = ttk.Frame(self.content_frame, padding=(240, 0, 0, 0), style='Content.TFrame')
        dashboard_frame.pack(fill=tk.X)

        # Dashboard buttons
        all_rice_button = ttk.Button(dashboard_frame, text="All Rice", command=self.display_all_rice, style='Content.TButton')
        all_rice_button.pack(side=tk.LEFT, padx=5)

        highsales_button = ttk.Button(dashboard_frame, text="High Sales", command=self.show_highsales_rice, style='Content.TButton')
        highsales_button.pack(side=tk.LEFT, padx=5)
        
        remove_button = ttk.Button(dashboard_frame, text="Remove ", command=self.remove_rice, style='Content.TButton')
        remove_button.pack(side=tk.LEFT, padx=5)
        
    # UPDATE
    def update_rice_details(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a detail to update.")
            return

        rice_info = self.tree.item(selected_item, 'values')
        rice_id = rice_info[0]

        # window para sa update
        self.update_rice_details_window = tk.Toplevel(self.content_frame)
        self.update_rice_details_window.title("Update Rice Details")

        # entry field sa rice sold in kg kasi siya lang need ng update
        rice_sold_kg_entry = tk.Entry(self.update_rice_details_window)

        tk.Label(self.update_rice_details_window, text="Rice Sold (in kg):").grid(row=0, column=0, padx=10, pady=5, sticky="e")

        rice_sold_kg_entry.grid(row=0, column=1, padx=30, pady=5)

        rice_sold_kg_entry.insert(0, rice_info[6])  # 6 yung value ng index kasi pang 7th column siya

        save_button = tk.Button(self.update_rice_details_window, text="Save Changes", command=lambda: self.save_updated_rice_info(
        rice_id, rice_sold_kg_entry.get()))
        save_button.grid(row=1, columnspan=2, pady=10)

        def clear_field():
            rice_sold_kg_entry.delete(0, 'end')

        clear_button = tk.Button(self.update_rice_details_window, text="Clear Field", command=clear_field)
        clear_button.grid(row=2, columnspan=2, pady=10)

    # SAVE UPDATED INFO
    def save_updated_rice_info(self, rice_id, rice_sold_kg):
        try:
            cursor = self.db_connection.cursor()

            select_query = "SELECT harvested_rice_kg FROM rice WHERE id=%s"
            cursor.execute(select_query, (rice_id,))
            result = cursor.fetchone()
            harvested_rice_kg = result[0] if result else 0

            rice_sold_kg = int(rice_sold_kg)

            # Calculation ng stocks and ales
            stocks = harvested_rice_kg - rice_sold_kg 
            price_per_kg = 50.00 
            sales = rice_sold_kg * price_per_kg

            query = "UPDATE rice SET rice_sold_kg=%s, stocks=%s, sales=%s WHERE id=%s"
            values = (rice_sold_kg, stocks, sales, rice_id)
            cursor.execute(query, values)

            self.db_connection.commit()
            messagebox.showinfo("Success", "Rice information updated successfully!")

            # Update the table with the updated rice information
            self.populate_table()
            self.update_rice_details_window.destroy()

        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Error updating rice information.")

        finally:
            if cursor:
                cursor.close()
    
        # REMOVE
 
    def remove_rice(self):
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a rice detail to delete.")
            return
        
        id = self.tree.item(selected_item)['values'][0]
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this rice detail?")
        
        if confirmation:
            delete_query="""DELETE FROM rice WHERE id = %s"""
            try:
                self.db_cursor.execute(delete_query, id)
                self.db_connection.commit()
                print("Deletion Successful")  
                messagebox.showinfo("Success", "Rice detail deleted successfully!")
                self.ricetracker_records()
                
            except Exception as e:
                print(f"Deletion Failed: {e}") 
                messagebox.showerror("Error", f"Failed to delete rice detail: {e}")

    def pagiling_ng_iba(self):
        self.clear_content_frame()

        self.db_cursor.execute("SELECT * FROM pagiling")
        rice = self.db_cursor.fetchall()
        
        self.clear_content_frame()
        
        title_label = tk.Label(self.content_frame, text="LIST OF ALL PAGILING", font=("Arial", 12, 'bold'))
        title_label.pack(pady=0)

        columns = ("ID", "Quantity of Rice (in kg)", "Date Received", "Sales")
        
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")

        # center
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.CENTER)

        # column widths
        self.tree.column("ID", width=10)  
        self.tree.column("Quantity of Rice (in kg)", width=100)  
        self.tree.column("Date Received", width=40)
        self.tree.column("Sales", width=80)
        
        for col in columns:
            self.tree.heading(col, text=col)

        # Insert data into the Treeview
        for rice in rice:
            self.tree.insert(parent='', index='end', iid=rice['id'], values=(
                rice['id'],
                rice['qty_of_rice_kg'],
                rice['date_received'],
                rice['sales']
            ))
            
        self.tree.pack(fill=tk.BOTH, expand=True, padx=0, pady=10)

        dashboard_frame = ttk.Frame(self.content_frame, padding=(215, 0, 0, 0), style='Content.TFrame')
        dashboard_frame.pack(fill=tk.X)

        # Dashboard buttons

if __name__ == "__main__":
    root = tk.Tk()
    login_page = LoginPage(root)
    root.mainloop()