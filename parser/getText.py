import json
from bs4 import BeautifulSoup as bs

file = "index.html"

with open(file, "r", encoding="utf-8") as f:
    file = f.read()

soup = bs(file, "html.parser")
soup.aside.extract()
content = soup.find('main',class_='page__main')

dumpster = []
for child in content.recursiveChildGenerator():
    if child.name and (child.name in ["h2", "p", "h1",'h3']):              
        string = child.text.replace("\n", "")
        string = string.replace("\t", "")
        if string == '':
            continue  
        if child.name == 'p' and len(child.text)<=5:
            continue
        if child.name in ['h1','h3']:
            dumpster.append({'h2': string})
            continue
        dumpster.append({child.name: string})

new_text =''
new_name = ''
article = []
for i,element in enumerate(dumpster):
    key= (*element,)[0]
    value = element[key]
    if new_name == '' and key == 'h2':
        new_name = value
        continue
    if new_name != '' and key == 'p':
        new_text += value
    if new_name != '' and key == 'h2':
        if new_text != '':
            article.append({new_name:new_text})
        new_name = value
        new_text = ''
        continue


with open("article.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(article,ensure_ascii=False))
