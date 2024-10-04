import json
import requests

data = {
    "name": "ivan",
    "age": "25",
    "friends": ["John", "Maria"],
    "owned_cars": [{"mark": "Kia", "hp": 100},{"mark": "Ford", "hp": 340}]
}
data = requests.get('https://evilinsult.com/generate_insult.php?type=json&lang=en')

data = data.text
data = json.loads(data)

print(data['insult'])

with open("data_file.json", "w") as write_file:
    json.dump(data, write_file)
