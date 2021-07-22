from tkinter import *
from detect_mask import *
from take_attendance import *
from datetime import datetime
import sqlite3
import pandas as pd


def welcome():
    window = Tk()
    window.title("Welcome")
    window.geometry("400x100")
    msg = Message(window, text="Welcome to Attendance System", justify="center")
    msg.pack()
    button1 = Button(window, text="Continue", command=wearMask)
    button1.pack(side=LEFT, padx=50)
    button2 = Button(window, text="STOP", command=quit)
    button2.pack(side=RIGHT, padx=50)
    window.mainloop()


def wearMask():
    check = check_mask()
    # check = True
    if check is True:
        optionsWindow()
    else:
        window = Tk()
        window.title("Message")
        window.geometry("300x100")
        msg = Message(window, text="Please wear your mask and try again")
        msg.pack()
        button1 = Button(window, text="Try Again", command=wearMask)
        button1.pack(side=LEFT, padx=50)
        button2 = Button(window, text="STOP", command=welcome)
        button2.pack(side=RIGHT, padx=50)
        window.mainloop()


def optionsWindow():
    window = Tk()
    window.title("Options")
    window.geometry("300x100")
    msg = Message(window, text="Are you a teacher or student")
    msg.pack()
    button1 = Button(window, text="Teacher", command=teacher)
    button1.pack(side=LEFT, padx=50)
    button2 = Button(window, text="Student", command=student)
    button2.pack(side=RIGHT, padx=50)
    window.mainloop()


def teacher():
    # Enter classID
    # The table with the given classID will be shown
    window = Tk()
    window.title("Teacher")
    window.geometry("800x200")
    msg = Message(window, text="Select the class name")
    msg.pack()

    def show():
        label.config(text=clicked.get())

    def display():
        classid = clicked.get()
        conn = sqlite3.connect("attendance.db")
        cur = conn.cursor()
        cur.execute('''SELECT * FROM ''' + classid)
        df = pd.read_sql('''SELECT * FROM ''' + classid, conn)

        df.to_csv('attendance.csv', index=False)

        conn.commit()
        conn.close()

        thankyou(1)

    options = [
        "CSE2004",
        "CSE3502",
        "ECM3002",
        "MGT1047",
        "ECM3003",
    ]

    clicked = StringVar()
    drop = OptionMenu(window, clicked, *options)
    drop.pack()
    button3 = Button(window, text="show class", command=show)
    button3.pack(side=LEFT, padx=50)

    # Create Label
    label = Label(window, text=" ")
    label.pack(side=LEFT, padx=60)

    button4 = Button(window, text="Download Attendance", width=30, command=display)
    button4.pack(side=RIGHT, padx=50)


def student():
    window = Tk()
    window.title("Student")
    window.geometry("800x200")
    msg = Message(window, text="Select you class")
    msg.pack()

    def show():
        label.config(text=clicked.get())

    def student2():
        # label.config(text=clicked.get())
        classid = clicked.get()
        name = take_attendance()
        # name = "Arnab Biswas 18BLC1152"
        only_name = name.split()
        full_name = only_name[0] + " " + only_name[1]
        reg_no = only_name[2]
        time_now = datetime.now()
        datetime_string = time_now.strftime('%H:%M:%S')
        # print(classid)
        # print(reg_no)
        # print(full_name)
        # print(datetime_string)

        conn = sqlite3.connect("attendance.db")
        cur = conn.cursor()
        cur.execute('''CREATE TABLE if not exists ''' + classid + '''
                (RegNo text PRIMARY KEY,
                Name text,
                Time text)
        ''')

        cur.execute("INSERT or IGNORE INTO " + classid + " (RegNo, Name, Time) VALUES(?,?,?)",
                    (reg_no, full_name, datetime_string))
        conn.commit()
        conn.close()

        thankyou(2)
        #
        # conn = sqlite3.connect("attendance.db")
        # c = conn.cursor()
        # c.execute("SELECT * FROM " + classid)
        # print(c.fetchall())

    options = [
        "CSE2004",
        "CSE3502",
        "ECM3002",
        "MGT1047",
        "ECM3003",
    ]

    clicked = StringVar()
    drop = OptionMenu(window, clicked, *options)
    drop.pack()
    button3 = Button(window, text="show class", command=show)
    button3.pack(side=LEFT, padx=50)

    # Create Label
    label = Label(window, text=" ")
    label.pack(side=LEFT, padx=60)

    button4 = Button(window, text="Give attendance", width=30, command=student2)
    button4.pack(side=RIGHT, padx=50)


def thankyou(number):
    window = Tk()
    window.title("Thank You")
    window.geometry("400x100")
    s = "Thank you"
    if number ==1:
        s +=" for downloading the attendance"
    else:
        s +=" for recording your attendance"
    msg = Message(window, text=s, justify="center")
    msg.pack()
    button = Button(window, text="STOP", command=quit)
    button.pack(side=RIGHT, padx=50)
    window.mainloop()


if __name__ == "__main__":
    welcome()
