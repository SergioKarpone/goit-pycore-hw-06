from collections import UserDict
from datetime import datetime, timedelta
from operator import itemgetter


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must have 10 digits")
        super().__init__(value)
    
    # Валідація номера телефону (10 цифр)
    @staticmethod
    def validate(phone):
        return phone.isdigit() and len(phone) == 10


class Birthday(Field):
    # Перевірка даних, перетворення у datetime
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


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
                raise ValueError("New phone number must have 10 digits")
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


class AddressBook(UserDict):
    
    # Додавання до адресної книги
    def add_record(self, record):
        self.data[record.name.value] = record
    
    # Пошук за ім'ям
    def find(self, name):
        return self.data.get(name)
    
    # Видалення запису за ім'ям
    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Contact {name} not found")
    
    # Список привітань на наступному тижні
    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.today().date()
        end_date = today + timedelta(days=6)

        for record in self.data.values():
            if not record.birthday:
                continue
            
            try:
                birthday = record.birthday.value.date()
            except Exception:
                print(f"Помилка формату дати для {record.name.value}. Пропускаємо.")
                continue

            # Встановлюємо рік дня народження на поточний рік
            birthday_this_year = birthday.replace(year=today.year)

            # Якщо день народження минув - наступний рік
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            # Перевірка потрапляння ДН у 7-днів
            if today <= birthday_this_year <= end_date:
                
                original_birthday = birthday_this_year
                congratulation_date = birthday_this_year
                
                day_of_week = birthday_this_year.weekday()

                # Обробка вихідних
                if day_of_week >= 5: 
                    # Переносимо привітання на наступний понеділок
                    if day_of_week == 5:  # Сб -> +2 дні
                        congratulation_date += timedelta(days=2)
                    elif day_of_week == 6:  # Нд -> +1 день
                        congratulation_date += timedelta(days=1)

                # До результату додаємо оригінальну дату
                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                    "original_birthday": original_birthday.strftime("%d.%m.%Y")
                })
        
        # Сортуємо за датою привітання
        sorted_birthdays = sorted(upcoming_birthdays, key=itemgetter('congratulation_date'))
        
        return sorted_birthdays


# Обробка помилок
def input_error(func):
    # Декоратор
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid command format."
        except Exception as e:
            return f"Error: {str(e)}"
    return inner


# Парсинг
def parse_input(user_input):
    # Введення користувача
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


@input_error

# Додавання або оновлення контакту
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


# Зміна телефону
@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


# Перелік телефонів
@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return str(record)


# Всі контакти
@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts found."
    return "\n".join(str(record) for record in book.data.values())


# Додавання дня народження
@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday)
    return "Birthday added."


# Показати день народження
@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    if record.birthday is None:
        return "Birthday not set for this contact."
    return f"{name}'s birthday: {record.birthday}"


# Дні народження на наступному тижні
@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    
    if not upcoming:
        return "No upcoming birthdays in the next week."
    
    # Поточна дата
    current_date = datetime.today().date()
    result = f"Дата сьогодні: {current_date.strftime('%d.%m.%Y')}\n\n"
    result += "Список привітань (за датою):\n"
    
    for item in upcoming:
        congrat_date = item['congratulation_date']
        original_date = item['original_birthday']
        
        output = f"{item['name']:<15} {congrat_date}"
        
        # Якщо дати відрізняються, показуємо оригінальну дату
        if congrat_date != original_date:
            output += f" (перенесено з {original_date})"
        
        result += output + "\n"
    
    return result.strip()


# Головна функція
def main():
    
    book = AddressBook()
    print("Welcome to the assistant bot!")
    
    # Обробка команд
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
