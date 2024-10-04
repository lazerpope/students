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
root.title("Casino")
root.geometry(f'366x300')
root['bg'] = '#949292'

photo = tk.PhotoImage(file='1.png')

tk.Label(text="1", bg="#555", image=photo, fg="#a3f4e7", bd=2,  font= ('Impact',15)).grid(row=1,column=0,stick = 'wens',padx=2,pady=3)
tk.Label(text="2", bg="#555",image=photo,  fg="#a3f4e7", bd=2,  font= ('Impact',15)).grid(row=1,column=1,stick = 'wens',padx=2,pady=3)
tk.Label(text="3", bg="#555", image=photo, fg="#a3f4e7", bd=2,  font= ('Impact',15)).grid(row=1,column=2,stick = 'wens',padx=2,pady=3)


tk.Button(text="Крутить", bg="#555", fg="#f4a3b0", bd=2, command = lambda:clear(), font= ('Impact',25)).grid(row=2,columnspan=3, column=0,stick = 'wens',padx=2,pady=3)

root.grid_columnconfigure(0,minsize=120)
root.grid_columnconfigure(1,minsize=120)
root.grid_columnconfigure(2,minsize=120)
root.grid_columnconfigure(3,minsize=120)

root.grid_rowconfigure(1,minsize=120)
root.grid_rowconfigure(2,minsize=120)
root.grid_rowconfigure(3,minsize=120)
root.grid_rowconfigure(4,minsize=120)
root.mainloop()