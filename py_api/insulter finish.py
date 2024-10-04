import tkinter as tk
import json
import requests
import math



def click():
    data = requests.get('https://evilinsult.com/generate_insult.php?type=json&lang=en')
    data = data.text
    data = json.loads(data)
    data = data['insult']       
        
   
    if len(data)<50:
        text.set(data) 
    elif len(data)<90:
        data = data.split()
        out = ''
        for i in range(len(data)):
            out += data[i] + ' '
            if i == int(len(data)/2):
                out+= '\n'
        text.set(out)
    else:
        data = data.split()
        out = ''
        for i in range(len(data)):
            out += data[i] + ' '
            if i == int(len(data ) /1.5):
                out+= '\n'
            if i == int(len(data ) /3):
                out+= '\n'

        text.set(out)
   

color_bg = "#E4E4E4"
color_dutton = "#AAAAAA"
color_snake = "#FCD335"
HEIGHT = 250
WIDTH = 450
root = tk.Tk()
root.title("Your personal insulter")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)
root['bg'] = color_bg


text = tk.StringVar()
text.set('Press The Button')
tk.Label(root,textvariable = text,  font = ('Oswald', 13, 'bold')).pack(fill=tk.BOTH, padx=2, pady=20)

tk.Button(root, command = lambda:click(), text = 'The Button',  font = ('Oswald', 27, 'bold')).pack( padx=2, pady=20)

root.mainloop()