import tkinter as tk
import json
import uuid
from tkcalendar import Calendar  # Import Calendar from tkcalendar library
import os


class User:
    def __init__(self, name, password, position):
        self.id = str(uuid.uuid4())  # Generate a unique id
        self.name = name
        self.password = password
        self.position = position

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'position': self.position
        }

    def register(self):
        try:
            with open('users.json', 'r') as file:
                user_data = json.load(file)
        except Exception:
            # If the file is not found, create an empty list
            user_data = []

        # Add the new user to the list
        user_data.append(self.to_dict())

        # Write the updated list to the file
        with open('users.json', 'w') as file:
            json.dump(user_data, file, ensure_ascii=False, indent=4)


class Service:
    def __init__(self, userId, name_service, period_access, geographic_zone, price):
        self.id = str(uuid.uuid4())
        self.userId = userId  # Corrected to use the user's ID
        self.name_service = name_service
        self.period_access = period_access
        self.geographic_zone = geographic_zone
        self.price = price

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'name_service': self.name_service,
            'period_access': self.period_access,
            'geographic_zone': self.geographic_zone
        }

    @classmethod
    def load_services(cls):
        try:
            with open('services.json', 'r') as file:
                services_data = json.load(file)
                if not services_data or not isinstance(services_data, list):
                    return []  # Return an empty list if the file is empty or not a list
                services = []
                for service_data in services_data:
                    service_name = service_data.get('name_service')
                    period_access = service_data.get('period_access')
                    geographic_zone = service_data.get('geographic_zone')
                    price = service_data.get('price', 0)  # Use a default price of 0 if 'price' is missing

                    # Check if any of the required fields is missing or if 'price' is not a valid number
                    if service_name and period_access and geographic_zone and isinstance(price, (int, float)):
                        services.append(cls(
                            service_data['userId'],
                            service_name,
                            period_access,
                            geographic_zone,
                            price
                        ))
                    else:
                        print(f"Invalid data format for service: {service_data}")
                return services
        except FileNotFoundError:
            return []

    def save_services(self):
        services = Service.load_services()
        services.append(self)
        with open('services.json', 'w') as file:
            json.dump([service.to_dict() for service in services], file, ensure_ascii=False, indent=4)


class App:
    def __init__(self, root):
        # Variable to store user choice
        self.position_var = tk.StringVar(value="Користувач")
        self.root = root
        self.root.title("Оформление послуг")
        self.registration_data = {}  # Dictionary to store user data

        # Create the initial registration/login screen
        self.create_login_screen()

    def create_registration_screen(self):
        # Remove all elements from the current screen (if any)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create and center elements using grid
        name_label = tk.Label(self.root, text="Ваше ім'я(логін):")
        self.name_entry = tk.Entry(self.root)
        email_label = tk.Label(self.root, text="Ваш пароль:")
        self.email_entry = tk.Entry(self.root)

        # Create radio buttons for selecting position
        position_label = tk.Label(self.root, text="Ваша посада:")
        user_radio = tk.Radiobutton(self.root, text="Користувач", variable=self.position_var, value="Користувач")
        customer_radio = tk.Radiobutton(self.root, text="Замовник", variable=self.position_var, value="Замовник")

        register_button = tk.Button(self.root, text="Зареєструватися", command=self.register_user)

        name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        email_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.email_entry.grid(row=1, column=1, padx=10, pady=10)

        position_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        user_radio.grid(row=2, column=1, padx=10, pady=10)
        customer_radio.grid(row=2, column=2, padx=10, pady=10)

        register_button.grid(row=3, column=0, columnspan=3, pady=10)

        # Center elements vertically and horizontally
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

    def register_user(self):
        name = self.name_entry.get()
        password = self.email_entry.get()
        position = self.position_var.get()  # Get the selected position value

        if name and password and position:
            self.registration_data['name'] = name
            self.registration_data['email'] = password
            self.registration_data['position'] = position

            new_user = User(name, password, position)
            new_user.register()
            if new_user.position == "Замовник":
                self.create_customer_window()
            else:
                self.create_service_provider_window()
        else:
            print("Заповніть усі поля.")

    def create_login_screen(self):
        # Remove all elements from the current screen (if any)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create and center elements using grid
        login_label = tk.Label(self.root, text="Логін:")
        self.login_entry = tk.Entry(self.root)
        password_label = tk.Label(self.root, text="Пароль:")
        self.password_entry = tk.Entry(self.root, show="*")
        login_button = tk.Button(self.root, text="Увійти", command=self.login)
        register_button = tk.Button(self.root, text="Зареєструватися", command=self.create_registration_screen)

        login_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.login_entry.grid(row=0, column=1, padx=5, pady=5)
        password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        login_button.grid(row=2, column=0, columnspan=2, pady=5)
        register_button.grid(row=3, column=0, columnspan=2)

        # Center elements vertically and horizontally
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        with open('users.json', 'r') as file:
            users_data = json.load(file)
        user_found = False
        for user_data in users_data:
            if user_data['name'] == login and user_data['password'] == password:
                user_found = True
                user_type = user_data['position']
                self.registration_data['name'] = user_data['name']
                self.registration_data['password'] = user_data['password']  # Changed 'email' to 'password'
                break
        if user_found:
            if user_type == "Замовник":
                self.create_customer_window()
            else:
                self.create_service_provider_window()
        else:
            print("Неправильний логін або пароль.")

    def create_customer_window(self):
        # Create the customer window
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Select a Geographic Zone:").pack()

        # Widget for selecting geographic zone
        geographic_zone_options = ["Ukraine", "Poland", "Bulgaria", "USA", "Germany"]
        self.geographic_zone_var = tk.StringVar()
        self.geographic_zone_var.set(geographic_zone_options[0])  # Default value
        geographic_zone_menu = tk.OptionMenu(self.root, self.geographic_zone_var, *geographic_zone_options)
        geographic_zone_menu.pack()

        tk.Button(self.root, text="Show Services", command=self.show_services).pack()

        tk.Label(self.root, text="Available Services:").pack()

        # Create and configure the service listbox
        self.service_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE,
                                          width=100)  # Change selectmode to SINGLE and set width
        self.service_listbox.pack()

        tk.Button(self.root, text="Process Selected Service", command=self.process_selected_service).pack()

        self.root.geometry("800x600")

        # Bind the listbox item selection to a callback function
        self.service_listbox.bind('<<ListboxSelect>>', self.process_selected_service)

    def process_selected_service(self):
        # Check if a service is selected
        if hasattr(self, 'selected_service'):
            # Process the selected service, e.g., display it or perform some action
            print(f"Processing selected service: {self.selected_service}")

            # Get the user's name
            user_name = self.registration_data.get('name', 'Unknown User')

            # Read the existing services from the services.json file
            services = Service.load_services()

            # Find the selected service by name
            selected_service = None
            for service in services:
                if service.name_service == self.selected_service:
                    selected_service = service
                    break

            if selected_service:
                # Remove the selected service from the list of services
                services.remove(selected_service)

                # Save the updated list of services back to services.json
                with open('services.json', 'w') as file:
                    json.dump([service.to_dict() for service in services], file, ensure_ascii=False, indent=4)

                # Create a dictionary for the accepted service
                accepted_service_data = {
                    'user_name': user_name,
                    'service_name': selected_service.name_service,
                    'geographic_zone': selected_service.geographic_zone,
                    'price': selected_service.price,
                    'period_access': selected_service.period_access,
                }

                # Append the accepted service to acceptedservices.json
                try:
                    with open('acceptedservices.json', 'r') as accepted_file:
                        accepted_data = json.load(accepted_file)
                except FileNotFoundError:
                    accepted_data = []

                accepted_data.append(accepted_service_data)

                with open('acceptedservices.json', 'w') as accepted_file:
                    json.dump(accepted_data, accepted_file, ensure_ascii=False, indent=4)

                print(f"Service '{selected_service.name_service}' has been accepted and removed from services.")
            else:
                print("Selected service not found.")
        else:
            print("No service selected.")

    def show_services(self):
        self.service_listbox.delete(0, tk.END)

        # Load services based on the selected geographic zone
        selected_zone = self.geographic_zone_var.get()
        services = Service.load_services()

        for service in services:
            if service.geographic_zone == selected_zone:
                # Format the service information
                service_info = f"Service Name: {service.name_service}, " \
                               f"Price: {service.price}, " \
                               f"Access Period: {service.period_access[0]} to {service.period_access[1]}"
                # Insert the formatted service information into the listbox
                self.service_listbox.insert(tk.END, service_info)

    def send_selected_services(self):
        selected_indices = self.service_listbox.curselection()

        if not selected_indices:
            print("No services selected.")
            return

        # Initialize a list to store selected service details
        selected_services_details = []

        for index in selected_indices:
            service_name = self.service_listbox.get(index)
            # Find the corresponding service object
            for service in self.services:
                if service.name_service == service_name:
                    selected_services_details.append(
                        f"Service Name: {service.name_service}, "
                        f"Region: {service.geographic_zone}, "
                        f"Price: {service.price}, "
                        f"Access Period: {service.period_access[0]} to {service.period_access[1]}"
                    )

        # Append the selected service details to the 'Accepted services' file
        with open('Accepted_services.txt', 'a') as file:
            file.write("Selected services for processing:\n")
            for service_details in selected_services_details:
                file.write(f"- {service_details}\n")
        print("Selected services have been sent for processing.")

    def create_service_provider_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Describe other interface elements you want to add on this screen
        tk.Label(self.root, text="Service Name:").pack()
        self.service_name_entry = tk.Entry(self.root)
        self.service_name_entry.pack()

        tk.Label(self.root, text="Access Period:").pack()
        self.period_start_cal = Calendar(self.root)
        self.period_start_cal.pack()
        self.period_end_cal = Calendar(self.root)
        self.period_end_cal.pack()

        tk.Label(self.root, text="Price:").pack()
        self.price_entry = tk.Entry(self.root)
        self.price_entry.pack()

        # Widget for selecting geographic zone
        tk.Label(self.root, text="Geographic Zone:").pack()
        geographic_zone_options = ["Ukraine", "Poland", "Bulgaria", "USA", "Germany"]
        self.geographic_zone_var = tk.StringVar()
        self.geographic_zone_var.set(geographic_zone_options[0])  # Default value
        geographic_zone_menu = tk.OptionMenu(self.root, self.geographic_zone_var, *geographic_zone_options)
        geographic_zone_menu.pack()

        tk.Button(self.root, text="Add Service", command=self.add_service).pack()

        # Create and configure the service list
        self.service_listbox = tk.Listbox(self.root, width=100)
        self.service_listbox.pack()

        # Populate the service list from the services.json file
        self.populate_service_listbox()
        self.root.geometry("700x800")

    def populate_service_listbox(self):
        if os.path.exists('services.json') and os.path.getsize('services.json') > 0:
            try:
                with open('services.json', 'r') as file:
                    services_data = json.load(file)
                    if not isinstance(services_data, list):
                        print("Invalid data format in 'services.json'.")
                        return

                    for service_data in services_data:
                        service_name = service_data.get('name_service')
                        price = service_data.get('price')
                        period_start, period_end = service_data.get('period_access')
                        if service_name and price and period_start and period_end:
                            service_info = f"Service Name: {service_name}, Price: {price}, " \
                                           f"Period: {period_start} to {period_end}"
                            self.service_listbox.insert(tk.END, service_info)
            except FileNotFoundError:
                print("Services file not found.")
        else:
            print("'services.json' is empty or does not exist.")

    def add_service(self):
        name = self.registration_data['name']
        service_name = self.service_name_entry.get()
        period_access = (self.period_start_cal.get_date(), self.period_end_cal.get_date())
        geographic_zone = self.geographic_zone_var.get()
        price = self.price_entry.get()  # Get the price from the entry field

        if service_name and period_access and geographic_zone and price:
            # Convert the price to a float (you can adjust the data type as needed)
            try:
                price = float(price)
            except ValueError:
                print("Price must be a valid number.")
                return

            new_service = Service(name, service_name, period_access, geographic_zone, price)
            new_service.save_services()
            self.service_name_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)  # Clear the price entry
            print("Послуга додана успішно.")
            self.service_listbox.insert(tk.END, f"Service Name: {service_name}, Price: {price}, "
                                                f"Period: {period_access[0]} to {period_access[1]}")
        else:
            print("Заповніть усі поля, включаючи ціну.")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    app = App(root)
    root.mainloop()
