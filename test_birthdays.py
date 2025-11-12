from assistant_bot import AddressBook, Record
from datetime import datetime, timedelta

# Тестування базового функціоналу
def test_basic_functionality():
        
    print("\nТестування боту\n")
    
    # Створення адресної книги
    book = AddressBook()
    print("\nАдресна книга створена")
    
    # Додавання контактів
    print("\nДодавання контактів...")
    
    # Контакт 1
    john = Record("John")
    john.add_phone("1234567890")
    john.add_birthday("15.03.1990")
    book.add_record(john)
    print("   ✓ Додано: John")
    
    # Контакт 2
    alice = Record("Alice")
    alice.add_phone("9876543210")
    # День народження через 3 дні від сьогодні
    future_date = (datetime.today() + timedelta(days=3)).strftime("%d.%m.%Y")
    alice.add_birthday(future_date)
    book.add_record(alice)
    print("Додано: Alice")
    
    # Контакт 3
    bob = Record("Bob")
    bob.add_phone("5551234567")
    # День народження в Сб (перенос на Пн)
    today = datetime.today()
    days_until_saturday = (5 - today.weekday()) % 7
    if days_until_saturday == 0:
        days_until_saturday = 7
    saturday_date = (today + timedelta(days=days_until_saturday)).strftime("%d.%m.%Y")
    bob.add_birthday(saturday_date)
    book.add_record(bob)
    print("Додано: Bob")
    
    # Показ всіх контактів
    print("\nВсі контакти:")
    for record in book.data.values():
        print(f"{record}")
    
    # Пошук контакту
    print("\nПошук контакту 'John':")
    found = book.find("John")
    if found:
        print(f"{found}")
    
    # Зміна телефону
    print("\nЗміна телефону для John:")
    john.edit_phone("1234567890", "5555555555")
    print(f"{book.find('John')}")
    
    # Додавання другого телефону
    print("\nДодавання другого телефону для John:")
    john.add_phone("9999999999")
    print(f"{book.find('John')}")
    
    # Показ днів народження
    print("\nДні народження на наступному тижні:")
    upcoming = book.get_upcoming_birthdays()
    if upcoming:
        for item in upcoming:
            congrat_date = item['congratulation_date']
            original_date = item['original_birthday']
            output = f"   {item['name']:<15} {congrat_date}"
            if congrat_date != original_date:
                output += f" (перенесено з {original_date})"
            print(output)
    else:
        print("Немає днів народження на наступному тижні")
    
    # Тестування валідації
    print("\nТестування валідації:")
    
    # Невірний телефон
    try:
        test_record = Record("Test")
        test_record.add_phone("123")
        print("Помилка: невірний телефон не був відхилений")
    except ValueError as e:
        print(f"Валідація телефону працює: {e}")
    
    # Невірна дата
    try:
        test_record = Record("Test2")
        test_record.add_birthday("2000-12-31")
        print("Помилка: невірна дата не була відхилена")
    except ValueError as e:
        print(f"Валідація дати працює: {e}")
    
    print("\nВсі тести - ОК!\n")


def test_edge_cases():
    # Тестування граничних випадків
    print("Тестування інших випадків")
    
    book = AddressBook()
    
    # Тест 1: Контакт без телефону
    print("\nКонтакт без телефону:")
    try:
        record = Record("NoPhone")
        book.add_record(record)
        print(f"{record}")
    except Exception as e:
        print(f"Помилка: {e}")
    
    # Тест 2: Контакт без дня народження
    print("\nКонтакт без дня народження:")
    try:
        record = Record("NoBirthday")
        record.add_phone("1234567890")
        book.add_record(record)
        print(f"{record}")
    except Exception as e:
        print(f"Помилка: {e}")
    
    # Тест 3: Видалення неіснуючого телефону
    print("\nВидалення неіснуючого телефону:")
    try:
        record = book.find("NoBirthday")
        record.remove_phone("9999999999")
        print("Помилка не була викликана")
    except ValueError as e:
        print(f"Обробка помилки працює: {e}")
    
    # Тест 4: Пошук неіснуючого контакту
    print("\nПошук неіснуючого контакту:")
    result = book.find("NonExistent")
    if result is None:
        print("Повернуто None для неіснуючого контакту")
    else:
        print("Помилка: знайдено неіснуючий контакт")
    
    print("Інші випадки оброблені правильно!")


if __name__ == "__main__":
    # Запуск тестів
    test_basic_functionality()
    test_edge_cases()
    
    print("Тестування пройдено!")
    print("\nДля запуску бота виконайте:")
    print("python assistant_bot.py")
