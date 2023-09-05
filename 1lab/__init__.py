import tkinter as tk
import json
import uuid


class User:
    def __init__(self, name, email, position):
        self.id = str(uuid.uuid4())  # Генерируем уникальный id
        self.name = name
        self.email = email
        self.position = position

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'position': self.position
        }

    def register(self):
        customer_data = self.to_dict()
        with open('users.json', 'a') as file:
            json.dump(customer_data, file)
            file.write('\n')


class Service:
    def __init__(self, name_service, period_access, geographic_zone):
        self.id = str(uuid.uuid4())
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
        service_data = self.to_dict()
        with open('services.json', 'a') as file:
            json.dump(service_data, file)
            file.write('\n')


class App:
    def __init__(self, root):
        self.email_entry = None
        self.name_entry = None
        self.password_entry = None
        self.login_entry = None
        self.root = root
        self.root.title("Оформление послуг")

        # Создание начального экрана регистрации/входа
        self.create_login_screen()

    def create_login_screen(self):
        # Удаление всех элементов текущего экрана (если они есть)
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Логин:").pack()
        self.login_entry = tk.Entry(self.root)
        self.login_entry.pack()

        tk.Label(self.root, text="Пароль:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Войти", command=self.login).pack()
        tk.Button(self.root, text="Зарегистрироваться", command=self.create_registration_screen).pack()

    def create_registration_screen(self):
        # Удаление всех элементов текущего экрана (если они есть)
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Ваше имя:").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        tk.Label(self.root, text="Ваш email:").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()

        tk.Label(self.root, text="Ваша должность:").pack()
        self.position_entry = tk.Entry(self.root)
        self.position_entry.pack()

        tk.Button(self.root, text="Зарегистрировать пользователя", command=self.register_user).pack()

    def login(self):
        # Здесь можно добавить логику проверки логина и пароля
        # Если вход успешен, перейдите на экран добавления услуг
        self.create_add_service_screen()

    def register_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        position = self.position_entry.get()

        if name and email and position:
            new_user = User(name, email, position)
            new_user.register()
            self.create_add_service_screen()
        else:
            print("Заполните все поля.")

    def create_add_service_screen(self):
        # Удаление всех элементов текущего экрана (если они есть)
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Название услуги:").pack()
        self.service_name_entry = tk.Entry(self.root)
        self.service_name_entry.pack()

        tk.Label(self.root, text="Период доступа:").pack()
        self.period_access_entry = tk.Entry(self.root)
        self.period_access_entry.pack()

        tk.Label(self.root, text="Географическая зона:").pack()
        self.geographic_zone_entry = tk.Entry(self.root)
        self.geographic_zone_entry.pack()

        tk.Button(self.root, text="Добавить услугу", command=self.add_service).pack()

    def add_service(self):
        service_name = self.service_name_entry.get()
        period_access = self.period_access_entry.get()
        geographic_zone = self.geographic_zone_entry.get()

        if service_name and period_access and geographic_zone:
            new_service = Service(service_name, period_access, geographic_zone)
            new_service.add_service()
            self.service_name_entry.delete(0, tk.END)
            self.period_access_entry.delete(0, tk.END)
            self.geographic_zone_entry.delete(0, tk.END)
            print("Услуга добавлена успешно.")
        else:
            print("Заполните все поля.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
