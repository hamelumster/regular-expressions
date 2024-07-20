from pprint import pprint
import csv
import re


# Читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)


# Обработка имен и фамилий
clear_contacts_list = []
for contact in contacts_list:
  full_name = " ".join(contact[:3]).split()
  while len(full_name) < 3:
    full_name.append("") #добавим пустые строки, если отчество или другие поля отсутствуют
  corrected_contact = full_name + contact[3:]
  clear_contacts_list.append(corrected_contact)

# Обработка номеров телефонов
pattern_phone = re.compile(
    r"(\+7|8)?\s*\(?(\d{3})\)?\s*(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})(\s*\(?доб\.\s*(\d+)\)?)?"
)

for contact in clear_contacts_list:
    contact[5] = pattern_phone.sub(lambda m: "+7({}){}-{}-{}{}".format(
        m.group(2), m.group(3), m.group(4), m.group(5),
        " доб.{}".format(m.group(7)) if m.group(7) else ""), contact[5])

# Удаление дубликатов
final_contacts = {}
for contact in clear_contacts_list:
  key = (contact[0], contact[1]) # Фамилия, Имя как ключи
  if key in final_contacts:
    # Объединяем информацию, если уже есть запись с таким же ключом
    existing_contact = final_contacts[key]
    for i in range(2, len(contact)): # Проходим по всем полям, включая отчество и остальные
      # Обновляем только если в новом контакте поле не пусто и в существующем контакте оно пусто
      if contact[i] and not existing_contact[i]:
        existing_contact[i] = contact[i]
  else:
    # Используем cope(), чтобы не менять один и тот же элемент списка
    final_contacts[key] = contact.copy()

# Преобразуем словарь обратно в список
final_contacts_list = list(final_contacts.values())

pprint(final_contacts_list)


# Код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(final_contacts_list)