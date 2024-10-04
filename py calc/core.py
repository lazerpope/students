import tkinter as tk
    

def add(num):
    value = calc.get() 
    if value == 'ERR':
        value =''
    if value == '0':
        value =value[:-1]
    calc.delete(0,tk.END)
    calc.insert(0,value+ str(num))

def oper(oper):
    value = calc.get() 
    if value[-1] in '+-*/':
        value =value[:-1]
    calc.delete(0,tk.END)
    calc.insert(0,value+oper)

def exec():
    value = calc.get() 
    calc.delete(0,tk.END)
    try:
        calc.insert(0,eval(value))
    except:
        calc.insert(0,'ERR')

def back():
    value = calc.get()     
    calc.delete(0,tk.END)
    if value[:-1] == '':
        calc.insert(0,'0')
    else:
        calc.insert(0,value[:-1])

def clear():    
    calc.delete(0,tk.END)
    calc.insert(0,'0')

def press_key(key):
    if key.char.isdigit():
        add(key.char)
    elif key.char in '+-*/':
        oper(key.char)
    elif key.char == '\r':
        exec()

root = tk.Tk() 
root.title("Calculator")
root.geometry(f'400x400')
root['bg'] = '#949292'

root.bind('<Key>',press_key)

calc = tk.Entry(root, justify=tk.RIGHT, font= ('Impact',15) )
calc.grid(row=0,column=0,columnspan=3 , stick = 'wens',padx=2,pady=3)
calc.insert(0,'0')

tk.Button(text="1", bg="#555", fg="#a3f4e7", bd=2, command = lambda:add(1), font= ('Impact',15)).grid(row=2,column=0,stick = 'wens',padx=2,pady=3)
tk.Button(text="2", bg="#555", fg="#a3f4e7", bd=2, command = lambda:add(2), font= ('Impact',15)).grid(row=2,column=1,stick = 'wens',padx=2,pady=3)
tk.Button(text="3", bg="#555", fg="#a3f4e7", bd=2, command = lambda:add(3), font= ('Impact',15)).grid(row=2,column=2,stick = 'wens',padx=2,pady=3)
tk.Button(text="4", bg="#555", fg="#a3f4e7", bd=2, command = lambda:add(4), font= ('Impact',15)).grid(row=3,column=0,stick = 'wens',padx=2,pady=3)
tk.Button(text="5", bg="#555", fg="#a3f4e7", bd=2, command = lambda:add(5), font= ('Impact',15)).grid(row=3,column=1,stick = 'wens',padx=2,pady=3)
tk.Button(text="6", bg="#555", fg="#a3f4e7", bd=2, command = lambda:add(6), font= ('Impact',15)).grid(row=3,column=2,stick = 'wens',padx=2,pady=3)
tk.Button(text="7", bg="#555", fg="#a3f4e7", bd=2, command = lambda:add(7), font= ('Impact',15)).grid(row=4,column=0,stick = 'wens',padx=2,pady=3)
tk.Button(text="8", bg="#555", fg="#a3f4e7", bd=2, command = lambda:add(8), font= ('Impact',15)).grid(row=4,column=1,stick = 'wens',padx=2,pady=3)
tk.Button(text="9", bg="#555", fg="#a3f4e7", bd=2, command = lambda:add(9), font= ('Impact',15)).grid(row=4,column=2,stick = 'wens',padx=2,pady=3)
tk.Button(text="0", bg="#555", fg="#a3f4e7", bd=2, command = lambda:add(0), font= ('Impact',15)).grid(row=5,column=0,stick = 'wens',padx=2,pady=3, columnspan=3)

tk.Button(text="+", bg="#555", fg="#f4a3b0", bd=2, command = lambda:oper("+"), font= ('Impact',15)).grid(row=1,column=3,stick = 'wens',padx=2,pady=3)
tk.Button(text="-", bg="#555", fg="#f4a3b0", bd=2, command = lambda:oper("-"), font= ('Impact',15)).grid(row=2,column=3,stick = 'wens',padx=2,pady=3)
tk.Button(text="*", bg="#555", fg="#f4a3b0", bd=2, command = lambda:oper("*"), font= ('Impact',15)).grid(row=3,column=3,stick = 'wens',padx=2,pady=3)
tk.Button(text="/", bg="#555", fg="#f4a3b0", bd=2, command = lambda:oper("/"), font= ('Impact',15)).grid(row=4,column=3,stick = 'wens',padx=2,pady=3)

tk.Button(text="=", bg="#555", fg="#f4e7a3", bd=2, command = lambda:exec(), font= ('Impact',15)).grid(row=5,column=3,stick = 'wens',padx=2,pady=3)

tk.Button(text="<<", bg="#555", fg="#f4a3b0", bd=2, command = lambda:back(), font= ('Impact',15)).grid(row=0,column=3,stick = 'wens',padx=2,pady=3)
tk.Button(text="CE", bg="#555", fg="#f4a3b0", bd=2, command = lambda:clear(), font= ('Impact',15)).grid(row=1,column=2,stick = 'wens',padx=2,pady=3)

root.grid_columnconfigure(0,minsize=80)
root.grid_columnconfigure(1,minsize=80)
root.grid_columnconfigure(2,minsize=80)
root.grid_columnconfigure(3,minsize=80)

root.grid_rowconfigure(1,minsize=60)
root.grid_rowconfigure(2,minsize=60)
root.grid_rowconfigure(3,minsize=60)
root.grid_rowconfigure(4,minsize=60)
root.mainloop()