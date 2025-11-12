# Модуль AddressBook

from collections import UserDict
from datetime import datetime, timedelta

# Клас для зберігання та управління контактами
class AddressBook(UserDict):
    
    # Додавання запису до адресної книги
    def add_record(self, record):
        self.data[record.name.value] = record
    
    # Пошук запису за іменем
    def find(self, name):
        return self.data.get(name)
    
    # Видалення запису за іменем
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

            birthday = record.birthday.value.date()

            # Рік дня народження - поточний рік
            birthday_this_year = birthday.replace(year=today.year)

            # Якщо ДН вже минув - на наступний рік
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            # Якшо ДН у 7 наступні днів
            if today <= birthday_this_year <= end_date:
                
                original_birthday = birthday_this_year
                congratulation_date = birthday_this_year
                
                day_of_week = birthday_this_year.weekday()

                # Якщо вихідні
                if day_of_week >= 5: 
                    # Переносимо привітання на Пн
                    if day_of_week == 5:  # Сб -> +2 дні
                        congratulation_date += timedelta(days=2)
                    elif day_of_week == 6:  # Нд -> +1 день
                        congratulation_date += timedelta(days=1)

                # Додаємо оригінальну дату
                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%Y.%m.%d"),
                    "original_birthday": original_birthday.strftime("%Y.%m.%d")
                })
        
        # Сортуємо за датою привітання
        upcoming_birthdays.sort(key=lambda x: x['congratulation_date'])
        
        return upcoming_birthdays
