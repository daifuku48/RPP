import tkinter as tk
import json
import uuid
from tkcalendar import Calendar
import os


class User:
    def __init__(self, name, password, position):
        self.id = str(uuid.uuid4())
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
        except FileNotFoundError:
            user_data = []

        user_data.append(self.to_dict())

        with open('users.json', 'w') as file:
            json.dump(user_data, file, ensure_ascii=False, indent=4)


class AcceptedService:
    def __init__(self, user_name, service_info):
        self.user_name = user_name
        self.service_info = service_info

    def to_dict(self):
        return {
            'user_name': self.user_name,
            'service_info': self.service_info
        }

    @classmethod
    def from_dict(cls, data):
        user_name = data.get('user_name')
        service_info = data.get('service_info')
        if user_name and service_info:
            return cls(user_name, service_info)
        return None


class Service:
    def __init__(self, userId, name_service, period_access, geographic_zone, price):
        self.id = str(uuid.uuid4())
        self.userId = userId
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
            'geographic_zone': self.geographic_zone,
            'price': self.price  # Добавлено поле 'price' для правильной записи
        }

    @staticmethod
    def load_services():
        services = []
        try:
            with open('services.json', 'r') as file:
                # Проверим, пуст ли файл
                file_contents = file.read()
                if file_contents.strip():  # Если файл не пуст
                    services_data = json.loads(file_contents)
                    if isinstance(services_data, list):
                        for service_data in services_data:
                            service = Service(
                                userId=service_data['userId'],
                                name_service=service_data['name_service'],
                                period_access=service_data['period_access'],
                                geographic_zone=service_data['geographic_zone'],
                                price=service_data['price']
                            )
                            services.append(service)
                    else:
                        print("Invalid data format in 'services.json'.")
                else:
                    print("'services.json' is empty.")
        except FileNotFoundError:
            print("'services.json' does not exist.")
        return services

    def save_services(self):
        services = Service.load_services()
        services.append(self)
        with open('services.json', 'w') as file:
            json.dump([service.to_dict() for service in services], file, ensure_ascii=False, indent=4)


class App:
    def __init__(self, root):
        self.position_var = tk.StringVar(value="Користувач")
        self.root = root
        self.root.title("Оформлення послуг")
        self.registration_data = {}

        self.create_login_screen()

    def create_registration_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        name_label = tk.Label(self.root, text="Ваше ім'я(логін):")
        self.name_entry = tk.Entry(self.root)
        email_label = tk.Label(self.root, text="Ваш пароль:")
        self.email_entry = tk.Entry(self.root)

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
        position = self.position_var.get()

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
        for widget in self.root.winfo_children():
            widget.destroy()

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
                self.registration_data['password'] = user_data['password']
                break
        if user_found:
            if user_type == "Замовник":
                self.create_customer_window()
            else:
                self.create_service_provider_window()
        else:
            print("Неправильний логін або пароль.")

    def create_customer_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Select a Geographic Zone:").pack()

        geographic_zone_options = ["Ukraine", "Poland", "Bulgaria", "USA", "Germany"]
        self.geographic_zone_var = tk.StringVar()
        self.geographic_zone_var.set(geographic_zone_options[0])
        geographic_zone_menu = tk.OptionMenu(self.root, self.geographic_zone_var, *geographic_zone_options)
        geographic_zone_menu.pack()

        tk.Button(self.root, text="Show Services", command=self.show_services).pack()

        tk.Label(self.root, text="Available Services:").pack()

        self.service_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width=80)
        self.service_listbox.pack()

        tk.Button(self.root, text="Process Selected Service", command=self.process_selected_service).pack()

        self.root.geometry("800x800")

        self.service_listbox.bind('<<ListboxSelect>>', self.on_service_selection)

    def on_service_selection(self, event):
        selected_indices = self.service_listbox.curselection()
        if selected_indices:
            self.selected_service_index = selected_indices[0]
        else:
            self.selected_service_index = None

    def process_selected_service(self):
        if self.selected_service_index is not None:
            selected_service = self.service_listbox.get(self.selected_service_index)
            selected_service_data = {
                'user_name': self.registration_data.get('name', 'Unknown User'),
                'service_info': selected_service
            }

            accepted_services = self.load_accepted_services()
            accepted_services.append(selected_service_data)
            self.save_accepted_services(accepted_services)

            self.remove_selected_service()
            print(f"Service '{selected_service}' has been accepted and removed from services.")
        else:
            print("No service selected.")

    def load_accepted_services(self):
        try:
            with open('acceptedservices.json', 'r') as file:
                accepted_data = json.load(file)
                if not accepted_data or not isinstance(accepted_data, list):
                    return []
                return accepted_data
        except FileNotFoundError:
            return []

    def save_accepted_services(self, accepted_data):
        with open('acceptedservices.json', 'w') as file:
            json.dump(accepted_data, file, ensure_ascii=False, indent=4)

    def remove_selected_service(self):
        selected_service = self.selected_service_index
        if selected_service is not None:
            services = Service.load_services()
            if 0 <= selected_service < len(services):
                del services[selected_service]
                Service.save_services(services)
                self.show_services()

    def show_services(self):
        self.service_listbox.delete(0, tk.END)

        selected_zone = self.geographic_zone_var.get()
        services = Service.load_services()

        for service in services:
            if service.geographic_zone == selected_zone:
                service_info = f"Service Name: {service.name_service}, " \
                               f"Price: {service.price}, " \
                               f"Access Period: {service.period_access[0]} to {service.period_access[1]}"
                self.service_listbox.insert(tk.END, service_info)

    def create_service_provider_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a frame for available services
        available_services_frame = tk.Frame(self.root)
        available_services_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a Label for available services
        tk.Label(available_services_frame, text="Available Services:").pack()

        # Create and configure the listbox for available services
        self.service_listbox = tk.Listbox(available_services_frame, width=100)
        self.service_listbox.pack(fill=tk.BOTH, expand=True)

        # Create a frame for accepted services
        accepted_services_frame = tk.Frame(self.root)
        accepted_services_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a Label for accepted services
        tk.Label(accepted_services_frame, text="Accepted Services:").pack()

        # Create and configure the listbox for accepted services
        self.accepted_service_listbox = tk.Listbox(accepted_services_frame, width=100)
        self.accepted_service_listbox.pack(fill=tk.BOTH, expand=True)

        # Populate both listboxes
        self.populate_service_listbox()
        self.populate_accepted_service_listbox()

        # Create a frame for service input fields
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create the rest of the UI elements within the input frame
        tk.Label(input_frame, text="Service Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.service_name_entry = tk.Entry(input_frame)
        self.service_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Access Period:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.period_start_cal = Calendar(input_frame)
        self.period_start_cal.grid(row=1, column=1, padx=5, pady=5)
        self.period_end_cal = Calendar(input_frame)
        self.period_end_cal.grid(row=1, column=2, padx=5, pady=5)

        tk.Label(input_frame, text="Price:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.price_entry = tk.Entry(input_frame)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Geographic Zone:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        geographic_zone_options = ["Ukraine", "Poland", "Bulgaria", "USA", "Germany"]
        self.geographic_zone_var = tk.StringVar()
        self.geographic_zone_var.set(geographic_zone_options[0])
        geographic_zone_menu = tk.OptionMenu(input_frame, self.geographic_zone_var, *geographic_zone_options)
        geographic_zone_menu.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(input_frame, text="Add Service", command=self.add_service).grid(row=4, column=0, columnspan=3,
                                                                                  pady=10)

        self.root.geometry("1000x800")

    def populate_accepted_service_listbox(self):
        # Clear the existing items in the listbox
        self.accepted_service_listbox.delete(0, tk.END)

        # Load the accepted services from the 'acceptedservices.json' file
        try:
            with open('acceptedservices.json', 'r') as file:
                accepted_services_data = json.load(file)
        except FileNotFoundError:
            accepted_services_data = []

        # Iterate through the accepted services and add them to the listbox
        for service_data in accepted_services_data:
            service_info = service_data.get('service_info')  # Retrieve the entire service info as a string

            if service_info:
                # Insert the formatted service information into the accepted service listbox
                self.accepted_service_listbox.insert(tk.END, service_info)

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
        price = self.price_entry.get()

        if service_name and period_access and geographic_zone and price:
            try:
                price = float(price)
            except ValueError:
                print("Price must be a valid number.")
                return

            new_service = Service(name, service_name, period_access, geographic_zone, price)
            new_service.save_services()
            self.service_name_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
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
