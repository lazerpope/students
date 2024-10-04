import json
from support import load_students, load_messages

messages_path = "class.html"
group_path = 'p31.txt'
students = load_students(group_path)
messages = load_messages(messages_path)

def trim_messages(message):
    message = message.replace('\n', '')
    message = message.replace('ответ от пользователя', '')
    message = message.replace(',', '')
    return message

messages  = list(map(trim_messages, messages))

students_dict_num = {}
students_dict_amount = {}
for student in students:
    students_dict_num.update({student: 0})
    students_dict_amount.update({student: 0})

for message in messages:
    for student in students:
        if message.find(student) != -1:
            students_dict_num[student] += 1 
            students_dict_amount[student] += len(message[0:message.find(student)]) 

# print(students_dict)

with open("num.json", "w", encoding="utf-8") as f:
    json.dump(students_dict_num, f, ensure_ascii=False, indent=4)
print("Success")

with open("amount.json", "w", encoding="utf-8") as f:
    json.dump(students_dict_amount, f, ensure_ascii=False, indent=4)
print("Success")
