from bs4 import BeautifulSoup as bs

def load_students(path):
    with open(path, "r", encoding="utf-8") as f:
        students = f.read()

    students = students.split("\n")

    for i,student in enumerate(students):
        students[i] = student.lower()
        students[i] = ''.join(students[i].split())
        if students[i] == '':
            students.pop(i)

    print (f'Загружено {len(students)} студентов')
    return students

def load_messages(path):
    with open(path, "r", encoding="utf-8") as f:
        html_doc = f.read()

    soup = bs(html_doc, "html.parser")

    arr = soup.find_all("div", {"class": "screen-reader-text"})

    data = []
    for i in arr: 
        string = i.text.lower()
        data.append(string)
    print (f'Загружено {len(data)} сообщений')
    return data