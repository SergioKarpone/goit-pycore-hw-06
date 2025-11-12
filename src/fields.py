# Модуль для класів полів

from datetime import datetime


# Базовий клас для полів запису
class Field:
    
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# Клас для зберігання імені контакту
class Name(Field):
    
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)


# Клас для зберігання телефонного номера
class Phone(Field):
    
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must have 10 digits")
        super().__init__(value)
    
    # Валідація номера телефону (10 цифр)
    @staticmethod
    def validate(phone):
        return phone.isdigit() and len(phone) == 10


# Клас для зберігання дня народження
class Birthday(Field):
    
    # Перевірка коректності даних та перетворення рядка на об'єкт datetime
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    
    # Формат YYYY.MM.DD для сумісності
    def __str__(self):
        
        return self.value.strftime("%Y.%m.%d")
