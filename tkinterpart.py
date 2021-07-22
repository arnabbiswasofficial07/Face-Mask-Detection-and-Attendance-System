from tkinter import *
name = "Arnab"
print(name)
window = Tk()
window.geometry("1000x1000")
window.title("Attendance")
window.geometry("300x100")
def func_print():
    name = name_label.get(1.0, "end-1c")
    print(name)
    label.config(text="Name"+name)

msg = Message(window, text="Enter your attendance", width=400)
msg.pack()
name_label = Text(window, height = 5, width = 10)

name_label.pack()
b = Button(window, text="take name", command=func_print)
b.pack()
label = Label(window)
label.pack()
window.mainloop()
print(name)




# if __name__="__main__":
#     createWindow()