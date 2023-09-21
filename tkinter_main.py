from tkinter import *
from tkinter import ttk

root = Tk()  # создаем корневой объект - окно
root.title("Технические индикаторы")  # устанавливаем заголовок окна
root.iconbitmap(default="image4.ico")
root.geometry("800x600")  # устанавливаем размеры окна
root.resizable(False, False)

btn = ttk.Button(text="Click")
btn.pack(anchor="nw", padx=340, pady=45, ipadx=15, ipady=15)

label = Label(root, text="Индикаторы", font=14)  # создаем текстовую метку
label.pack(anchor="center", pady=150, fill=X)  # размещаем метку в окне

root.mainloop()
