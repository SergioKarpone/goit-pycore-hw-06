# Модуль для класу Record

from .fields import Name, Phone, Birthday


# Клас для зберігання інформації про контакт
class Record:
    
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # Додавання телефону
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    # Видалення телефону
    def remove_phone(self, phone):
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone {phone} not found")
    
    # Редагування телефону
    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            # Валідуємо новий номер
            if not Phone.validate(new_phone):
                raise ValueError("New phone number must contain exactly 10 digits")
            phone_to_edit.value = new_phone
        else:
            raise ValueError(f"Phone {old_phone} not found")
    
    # Пошук телефону
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    # Додавання дня народження
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"
