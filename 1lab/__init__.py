import tkinter as tk
import json
import uuid


class User:
    def __init__(self, name, password, position):
        self.id = str(uuid.uuid4())  # Генерируем уникальный id
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
            # Если файл не найден, создаем пустой список
            user_data = []

        # Добавляем нового пользователя в список
        user_data.append(self.to_dict())

        # Записываем обновленный список в файл
        with open('users.json', 'w') as file:
            json.dump(user_data, file, ensure_ascii=False, indent=4)


class Service:
    def __init__(self, userId, name_service, period_access, geographic_zone):
        self.id = str(uuid.uuid4())
        self.userId = userId
        self.name_service = name_service
        self.period_access = period_access
        self.geographic_zone = geographic_zone

    def to_dict(self):
        return {
            'id': self.id,
            'name_service': self.name_service,
            'period_access': self.period_access,
            'geographic_zone': self.geographic_zone
        }

    def add_service(self):
        try:
            with open('services.json', 'r') as file:
                service_data = json.load(file)
        except Exception:
            # Если файл не найден, создаем пустой список
            service_data = []

        # Добавляем нового пользователя в список
        service_data.append(self.to_dict())

        # Записываем обновленный список в файл
        with open('services.json', 'w') as file:
            json.dump(service_data, file, ensure_ascii=False, indent=4)


class App:
    def __init__(self, root):
        # Переменная для хранения выбора пользователя
        self.position_var = tk.StringVar(value="Користувач")
        self.root = root
        self.root.title("Оформление послуг")
        self.registration_data = {}  # Словарь для хранения данных пользователя

        # Создание начального экрана регистрации/входа
        self.create_login_screen()

    def create_registration_screen(self):
        # Удаление всех элементов текущего экрана (если они есть)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Создаем и центрируем элементы с помощью grid
        name_label = tk.Label(self.root, text="Ваше ім'я(логін):")
        self.name_entry = tk.Entry(self.root)
        email_label = tk.Label(self.root, text="Ваш пароль:")
        self.email_entry = tk.Entry(self.root)

        # Создаем радиокнопки для выбора позиции
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

        # Центрируем элементы по вертикали и горизонтали
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
        position = self.position_var.get()  # Получаем выбранное значение позиции

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
        # Удаление всех элементов текущего экрана (если они есть)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Создаем и центрируем элементы с помощью grid
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

        # Центрируем элементы по вертикали и горизонтали
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
                self.registration_data['email'] = user_data['email']
                break
        if user_found:
            if user_type == "Замовник":
                self.create_customer_window()
            else:
                self.create_service_provider_window()
        else:
            print("Неправильний логін або пароль.")

    def create_customer_window(self):
        # Создание окна замовника
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_service_provider_window(self):
        # Создание окна користувача
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Название послуги:").pack()
        self.service_name_entry = tk.Entry(self.root)
        self.service_name_entry.pack()

        tk.Label(self.root, text="Період доступу:").pack()
        self.period_access_entry = tk.Entry(self.root)
        self.period_access_entry.pack()

        tk.Label(self.root, text="Географічна зона:").pack()
        self.geographic_zone_entry = tk.Entry(self.root)
        self.geographic_zone_entry.pack()

        tk.Button(self.root, text="Додати послугу", command=self.add_service).pack()

        # Create a Listbox widget
        self.service_listbox = tk.Listbox(self.root)
        self.service_listbox.pack()

        # Populate the Listbox with existing services
        self.populate_service_listbox()

    def populate_service_listbox(self):
        # You need to read the existing services from 'services.json' and add them to the Listbox
        try:
            with open('services.json', 'r') as file:
                services_data = json.load(file)
                for service_data in services_data:
                    service_name = service_data['name_service']
                    self.service_listbox.insert(tk.END, service_name)
        except FileNotFoundError:
            print("Services file not found.")

    def add_service(self):
        name = self.name_entry.get()
        service_name = self.service_name_entry.get()
        period_access = self.period_access_entry.get()
        geographic_zone = self.geographic_zone_entry.get()

        if service_name and period_access and geographic_zone:
            new_service = Service(name, service_name, period_access, geographic_zone)
            new_service.add_service()
            self.service_name_entry.delete(0, tk.END)
            self.period_access_entry.delete(0, tk.END)
            self.geographic_zone_entry.delete(0, tk.END)
            print("Послуга додана успішно.")
            # Update the Listbox with the new service
            self.service_listbox.insert(tk.END, service_name)
            new_service.add_service()
        else:
            print("Заповніть усі поля.")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    app = App(root)
    root.mainloop()