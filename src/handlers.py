# Модуль обробників команд

from .utils import input_error
from .record import Record
from .address_book import AddressBook


# Додавання або оновлення контакту
@input_error
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


# Зміна телефону контакту
@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


# Показати телефон контакту
@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return str(record)


# Показати всі контакти
@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts found."
    return "\n".join(str(record) for record in book.data.values())


# Додавання дня народження до контакту
@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday)
    return "Birthday added."


# Показати день народження контакту
@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    if record.birthday is None:
        return "Birthday not set for this contact."
    return f"{name}'s birthday: {record.birthday}"


# Показати дні народження на наступному тижні
@input_error
def birthdays(args, book: AddressBook):
    
    from datetime import datetime, timedelta
    upcoming = book.get_upcoming_birthdays()
    
    # Поточна дата
    current_date = datetime.today().date()
    
    print(f"\nДата сьогодні: {current_date.strftime('%Y.%m.%d')}")
    
    if not upcoming:
        return "На наступний тиждень привітань немає."
    
    print("\nСписок привітань (за датою):")
    result_lines = []
    
    for item in upcoming:
        congrat_date = item['congratulation_date']
        original_date = item['original_birthday']
        
        output = f"{item['name']:<15} {congrat_date}"
        
        # Якщо дати відрізняються, показуємо оригінальну дату
        if congrat_date != original_date:
            output += f" (перенесено з {original_date})"
        
        result_lines.append(output)
    
    return "\n".join(result_lines)
