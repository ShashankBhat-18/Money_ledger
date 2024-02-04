from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3
import csv
import os
from datetime import date
import shutil


root = Tk()
root.title("Money Ledger")
root.geometry("413x500")
root['background'] = '#000000'


heading = Label(root, text="WELCOME TO MONEY LEDGER!", font=("Helvatica", 18,
                "bold", "underline"), highlightbackground='#FFFFFF', bg="#000000", fg="#FFFFFF")
heading.grid(column=0, row=0,pady=15)

frame = LabelFrame(root, text="Choose", fg="#96DED1",
                   padx=10, pady=25, bg="#000000")
frame.grid(column=0, row=1, padx=5, pady=25)


def money():
    root = Tk()
    root.title("Money Ledger")

    root['background'] = '#000000'

    conn = sqlite3.connect("money_book.db")
    c = conn.cursor()

    '''c.execute("""CREATE TABLE moneys (
            first_name text,
            last_name text,
            city text,
            money_borrowed integer,
            money_lent integer,
            rate integer,
            time integer
            )""")'''

    def update():
        conn = sqlite3.connect("money_book.db")
        c = conn.cursor()
        record_id = delete_box.get()
        c.execute("""UPDATE moneys SET
                  first_name=:first,
                  last_name=:last,
                  city=:city,
                  money_borrowed=:bmoney,
                  money_lent=:lmoney
              
                WHERE oid = :oid""",
                  {
                      'first': f,
                      "last": l,
                      "city": cities,
                      "bmoney": mo,
                      "lmoney": money_lent_editor.get(),
                      "oid": record_id
                  })

        conn.commit()

        conn.close()

        editor.destroy()

    def submit():
        conn = sqlite3.connect("money_book.db")
        c = conn.cursor()
        c.execute("INSERT INTO moneys VALUES(:f_name,:lname,:city,:money_borrowed,:money_lent,:rate,:time)",
                  {
                      'f_name': f_name.get(),
                      "lname": lname.get(),
                      "city": city.get(),
                      "money_borrowed": Principlea.get(),
                      "money_lent": ci.get(),
                      "rate": rate.get(),
                      "time": time.get()
                  })

        conn.commit()

        conn.close()

        f_name.delete(0, END)
        lname.delete(0, END)
        city.delete(0, END)
        Principlea.delete(0, END)
        ci.delete(0, END)
        rate.delete(0, END)
        time.delete(0, END)

    def query():
        conn = sqlite3.connect("money_book.db")
        c = conn.cursor()
        c.execute("SELECT*,oid FROM moneys")
        records = c.fetchall()
        print_records = ''
        numbers = ''
        for record in records:
            print_records += str(record[0])+"\n"
            numbers += str(record[7])+"\n"
            querylbl = Label(root, text=print_records,
                             justify=LEFT, bg="#000000", fg="#FFFFFF")
            querylbl.grid(row=15, column=0, columnspan=2)
            numberlbl = Label(root, text=numbers,
                              justify=RIGHT, bg="#000000", fg="#FFFFFF")
            numberlbl.grid(row=15, column=1)

        conn.commit()

        conn.close()

    def delete():
        try:
            conn = sqlite3.connect("money_book.db")
            c = conn.cursor()
            c.execute("DELETE FROM moneys WHERE oid="+delete_box.get())

            delete_box.delete(0, END)
            conn.commit()

            conn.close()
        except:
            response = messagebox.showerror(
                "You have not entered Id", "Please Enter ID  ")

    def edit():
        global f_name_editor
        global lname_editor
        global city_editor
        global money_borrowed_editor
        global money_lent_editor
        global rate_editor
        global time_editor
        global editor

        try:
            conn = sqlite3.connect("money_book.db")
            c = conn.cursor()
            editor = Tk()
            editor.title("Detailed report")

            editor.geometry("192x200")
            editor["background"] = '#000000'

            conn = sqlite3.connect("money_book.db")
            c = conn.cursor()
            recordid = delete_box.get()
            c.execute("SELECT* FROM moneys WHERE oid=" + recordid)
            records = c.fetchall()
            print(records)
            print_records = ''
            for record in records:
                for j in record:
                    print_records += str(j)+"\n"

            for record in records:
                global f
                global l
                global cities
                global mo
                global rss
                global tss

                f = (record[0])
                l = (record[1])
                cities = (record[2])
                mo = (record[3])
                ml = (record[4])
                rss = (record[5])
                tss = (record[6])

            f_name_editor = Label(editor, text=f, bg="#000000", fg="#FFFFFF")
            f_name_editor.grid(column=1, row=0, padx=20)

            lname_editor = Label(editor, text=l, bg="#000000", fg="#FFFFFF")
            lname_editor.grid(column=1, row=1)

            city_editor = Label(editor, text=cities,
                                bg="#000000", fg="#FFFFFF")
            city_editor.grid(column=1, row=2)

            money_borrowed_editor = Label(
                editor, text=mo, bg="#000000", fg="#FFFFFF")
            money_borrowed_editor.grid(column=1, row=3)

            money_lent_editor = Label(
                editor, text=ml, bg="#000000", fg="#FFFFFF")
            money_lent_editor.grid(column=1, row=4, pady=2)

            rate_editor = Label(editor, text=rss, bg="#000000", fg="#FFFFFF")
            rate_editor.grid(column=1, row=5, pady=2)

            time_editor = Label(editor, text=tss, bg="#000000", fg="#FFFFFF")
            time_editor.grid(column=1, row=6, pady=2)

            ratel = Label(editor, text="Rate(%)", bg="#000000", fg="#FFFFFF")
            ratel.grid(row=5, column=0)

            timel = Label(editor, text="Time (Years)",
                          bg="#000000", fg="#FFFFFF")
            timel.grid(row=6, column=0)

            f_namel = Label(editor, text="First name",
                            bg="#000000", fg="#FFFFFF")
            f_namel.grid(row=0, column=0)

            lnamel = Label(editor, text="Last name",
                           bg="#000000", fg="#FFFFFF")
            lnamel.grid(row=1, column=0)

            cityl = Label(editor, text="City", bg="#000000", fg="#FFFFFF")
            cityl.grid(row=2, column=0)

            money_borrowedl = Label(
                editor, text="Principle Amount", bg="#000000", fg="#FFFFFF")
            money_borrowedl.grid(row=3, column=0)

            money_lentl = Label(
                editor, text="Compound Interest", bg="#000000", fg="#FFFFFF")
            money_lentl.grid(row=4, column=0)

            spacer1 = Label(editor, text="", bg="#000000")
            spacer1.grid(row=9, column=0)

            status = Label(editor, text="Detailed report", bd=1,
                           relief=SUNKEN, anchor=N, fg="#96DED1", bg="#28282B")
            status.grid(column=0, row=10, columnspan=7, sticky="WE")

        except:
            response = messagebox.showerror(
                "You have not entered Id", "Please Enter ID  ")

    def calc_ci():
        global rat
        ci.delete(0, END)
        principle = int(Principlea.get())

        rat = float(rate.get())
        t = int(time.get())
        Comp = round(principle * (pow((1 + rat / 100), t)))
        ci.insert(10, Comp)

    f_name = Entry(root, width=30, bg="#87CEEB", bd=2)
    f_name.grid(column=1, row=0, padx=20, pady=2)

    lname = Entry(root, width=30, bg="#87CEEB", bd=2)
    lname.grid(column=1, row=1, pady=2)

    city = Entry(root, width=30, bg="#87CEEB", bd=2)
    city.grid(column=1, row=3, pady=2)

    Principlea = Entry(root, width=30, bg="#87CEEB", bd=2)
    Principlea.grid(column=1, row=4, pady=2)

    rate = Entry(root, width=30, bg="#87CEEB", bd=2)
    rate.grid(column=1, row=5, pady=2)

    time = Entry(root, width=30, bg="#87CEEB", bd=2)
    time.grid(column=1, row=6, pady=2)

    ci = Entry(root, width=30, bg="#87CEEB", bd=2)
    ci.grid(column=1, row=7, pady=2)

    delete_box = Entry(root, width=30, bg="#87CEEB", bd=2)
    delete_box.grid(row=11, column=1, pady=5)

    f_namel = Label(root, text="First name", bg="#000000", fg="#FFFFFF")
    f_namel.grid(row=0, column=0)

    lnamel = Label(root, text="Last name", bg="#000000", fg="#FFFFFF")
    lnamel.grid(row=1, column=0)

    cityl = Label(root, text="City", bg="#000000", fg="#FFFFFF")
    cityl.grid(row=3, column=0)

    Principleal = Label(root, text="Money Borrowed",
                        bg="#000000", fg="#FFFFFF")
    Principleal.grid(row=4, column=0)

    ratel = Label(root, text="Rate(%)", bg="#000000", fg="#FFFFFF")
    ratel.grid(row=5, column=0)

    timel = Label(root, text="Time (Years)", bg="#000000", fg="#FFFFFF")
    timel.grid(row=6, column=0)

    ans = Button(root, text="Submit", bg="#50C878", command=calc_ci)
    ans.grid(row=8, column=1, pady=10)

    cil = Label(root, text="Compound Interest", bg="#000000", fg="#FFFFFF")
    cil.grid(row=7, column=0)

    deletebox = Label(root, text="Select ID", bg="#000000", fg="#FFFFFF")
    deletebox.grid(row=11, column=0, pady=5)

    submitbtn = Button(root, text="Add record to database",
                       command=submit, bg="#50C878")
    submitbtn.grid(row=9, column=0, columnspan=2, padx=10, pady=10, ipadx=113)

    querybtn = Button(root, text="Show Records", bg="#50C878", command=query)
    querybtn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

    deletebtn = Button(root, text="Delete Records",
                       bg="#50C878", command=delete)
    deletebtn.grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=135)

    Editbtn = Button(root, text="Detailed report", bg="#50C878", command=edit)
    Editbtn.grid(row=13, column=0, columnspan=2, pady=10, padx=10, ipadx=142)

    spacer1 = Label(root, text="", bg="#000000")
    spacer1.grid(row=14, column=0)

    status = Label(root, text="Money Ledger", bd=1, relief=SUNKEN,
                   anchor=N, fg="#96DED1", bg="#28282B")
    status.grid(column=0, row=17, columnspan=7, sticky="WE")

    conn.commit()

    conn.close()

    root.mainloop()


def expense():
    today = date.today()
    l1 = []
    if not os.path.exists('tempDir'):
        os.makedirs('tempDir')

    def show_entry_fields():
        f2 = open(r"Expenses.txt", "a")
        global l
        str = ("\n")

        l1.append((e2.get()))
        L = [(e2.get()), str]

        mainfile = open(r"Main report.txt", "a")
        lin = variable.get()
        li = (e2.get())
        mainfile.write(lin)
        mainfile.write(li)
        mainfile.write("\n")

        if (variable.get()) == "Food":
            f3 = open(r"tempDir/Expense.txt", "a")
            L = [(e2.get()), str]
            f3.writelines(L)
            f3.close()
        elif (variable.get()) == "Grocery":
            f4 = open(r"tempDir/Expens.txt", "a")
            L = [(e2.get()), str]
            f4.writelines(L)
            f4.close()
        elif (variable.get()) == "Clothing and Footwear":
            f5 = open(r"tempDir/Expen.txt", "a")
            L = [(e2.get()), str]
            f5.writelines(L)
            f5.close()
        elif (variable.get()) == "Transport":
            f6 = open(r"tempDir/Expe.txt", "a")
            L = [(e2.get()), str]
            f6.writelines(L)
            f6.close()
        elif (variable.get()) == "Water":
            f7 = open(r"tempDir/Exp.txt", "a")
            L = [(e2.get()), str]
            f7.writelines(L)
            f7.close()
        elif (variable.get()) == "Electricity":
            f8 = open(r"tempDir/Ex.txt", "a")
            L = [(e2.get()), str]
            f8.writelines(L)
            f8.close()
        elif (variable.get()) == "Others":
            f9 = open(r"tempDir/E.txt", "a")
            L = [(e2.get()), str]
            f9.writelines(L)
            f9.close()

        f2.writelines(L)

        f2.close()

        e2.delete(0, 100)

    def monthly():
        try:
            fileobj = open(r"Expenses.txt")
            lines = []
            for line in fileobj:
                lines.append(line.strip())
                mapp = map(int, lines)
            lisst = list(mapp)
            T = (sum(lisst))

            maste = Tk()
            maste.title('Monthly report')
            maste.geometry("400x150")
            maste.configure(bg='grey')

            def mast():
                mast = Tk()
                mast.title('Detailed')
                mast.geometry("400x450")
                mast.configure(bg='grey')

                fileobj = open(r"tempDir/Expense.txt", 'a+')
                fileobj.seek(0)
                lines = []
                for line in fileobj:
                   lines.append(line.strip())
                mapp = map(int, lines)
                lisst = list(mapp)
                F = (sum(lisst))

                fileobj = open(r"tempDir/Expens.txt", 'a+')
                fileobj.seek(0)
                lines = []
                for line in fileobj:
                    lines.append(line.strip())
                a = map(int, lines)
                lisst = list(a)
                G = (sum(lisst))

                fileobj = open(r"tempDir/Expen.txt", 'a+')
                fileobj.seek(0)
                lines = []
                for line in fileobj:
                    lines.append(line.strip())
                    mapp = map(int, lines)
                lisst = list(mapp)
                H = (sum(lisst))

                fileobj = open(r"tempDir/Expe.txt", 'a+')
                fileobj.seek(0)
                lines = []
                for line in fileobj:
                    lines.append(line.strip())
                mapp = map(int, lines)
                lisst = list(mapp)
                I = (sum(lisst))

                fileobj = open(r"tempDir/Exp.txt", 'a+')
                fileobj.seek(0)
                lines = []
                for line in fileobj:
                    lines.append(line.strip())
                mapp = map(int, lines)
                lisst = list(mapp)
                J = (sum(lisst))

                fileobj = open(r"tempDir/Ex.txt", 'a+')
                fileobj.seek(0)
                lines = []
                for line in fileobj:
                    lines.append(line.strip())
                mapp = map(int, lines)
                lisst = list(mapp)
                K = (sum(lisst))

                fileobj = open(r"tempDir/E.txt", 'a+')
                fileobj.seek(0)
                lines = []
                for line in fileobj:
                    lines.append(line.strip())
                mapp = map(int, lines)
                lisst = list(mapp)
                L = (sum(lisst))
                if F != 0:
                    stre = ("FOOD:")
                    label = Label(mast, text=stre, font="Times", bg="grey")
                    label.place_configure(relx=0.2, rely=0.2, anchor='center')
                    label = Label(mast, text=F, font="Times", bg="grey")
                    label.place_configure(relx=0.6, rely=0.2, anchor='center')
                if G != 0:
                    stre = ("Grocery:")
                    label = Label(mast, text=stre, font="Times", bg="grey")
                    label.place_configure(relx=0.2, rely=0.3, anchor='center')
                    label = Label(mast, text=G, font="Times", bg="grey")
                    label.place_configure(relx=0.6, rely=0.3, anchor='center')
                if H != 0:
                    stre = ("Clothing and Footwear")
                    label = Label(mast, text=stre, font="Times", bg="grey")
                    label.place_configure(relx=0.2, rely=0.4, anchor='center')
                    label = Label(mast, text=H, font="Times", bg="grey")
                    label.place_configure(relx=0.6, rely=0.4, anchor='center')
                if I != 0:
                    stre = ("Transport")
                    label = Label(mast, text=stre, font="Times", bg="grey")
                    label.place_configure(relx=0.2, rely=0.5, anchor='center')
                    label = Label(mast, text=I, font="Times", bg="grey")
                    label.place_configure(relx=0.6, rely=0.5, anchor='center')
                if J != 0:
                    stre = ("Water")
                    label = Label(mast, text=stre, font="Times", bg="grey")
                    label.place_configure(relx=0.2, rely=0.6, anchor='center')
                    label = Label(mast, text=J, font="Times", bg="grey")
                    label.place_configure(relx=0.6, rely=0.7, anchor='center')
                if K != 0:
                    stre = ("Electricity")
                    label = Label(mast, text=stre, font="Times", bg="grey")
                    label.place_configure(relx=0.2, rely=0.8, anchor='center')
                    label = Label(mast, text=K, font="Times", bg="grey")
                    label.place_configure(relx=0.6, rely=0.8, anchor='center')
                if L != 0:
                    stre = ("Other:")
                    label = Label(mast, text=stre, font="Times", bg="grey")
                    label.place_configure(relx=0.2, rely=0.9, anchor='center')
                    label = Label(mast, text=L, font="Times", bg="grey")
                    label.place_configure(relx=0.6, rely=0.9, anchor='center')

            e2.grid(row=2, column=1, sticky=W)
            button = Button(maste, text='show detailed report', command=mast, bd=2,
                            fg="white",
                            bg="#202225",
                            font="Times",
                            height=1,
                            width=16,
                            highlightcolor="purple",
                            justify="right",
                            padx=4,
                            pady=8,
                            relief="raised")
            button.place_configure(relx=0.5, rely=0.8, anchor='center')
            stre = ("This month you've spent: $")
            label = Label(maste, text=stre, font="Times", bg="grey")
            label.place_configure(relx=0.5, rely=0.5, anchor='center')
            label = Label(maste, text=T, font="Times", bg="grey")
            label.place_configure(relx=0.9, rely=0.5, anchor='center')
            fileobj.close()
            maste.mainloop()
        except FileNotFoundError:
            messagebox.showerror("Data not found", "No records found!")

    master = Tk()
    master.title('Expenditure Tracker')
    master.geometry("445x160")
    master.configure(bg='#202225')
    master.resizable(False, False)

    variable = StringVar(master)
    variable.set("Select Category")  # default value
    wi = OptionMenu(master, variable, "Food", "Grocery", "Clothing and Footwear", "Transport", "Water", "Electricity",
                    "Others").grid(row=1, column=1, sticky=W, pady=5)

    Label(master, text="Select category:", font="Times", anchor=CENTER, fg="white", height=1, bg="#202225",
          width=12).grid(row=1)
    Label(master, text="Item Price:", font="Times", anchor=CENTER, fg="white", bg="#202225", height=1, width=10).grid(
        row=2, sticky=W)

    def reset():
        try:
            os.remove(r"Expenses.txt")
            shutil.rmtree("tempDir")
            os.remove(r"Main report.txt")
        except FileNotFoundError:
            messagebox.showerror("Data not found", "No file found!")

    reset_btn = Button(master, text="Reset", command=reset, height=1, width=7)
    # put on screen
    reset_btn.grid(row=3, column=2)
    lobol = Label(master, text=today, bg="#202225", fg="white")
    lobol.config(font=("Courier", 14))
    lobol.grid(row=1, column=2)
    e2 = Entry(master)
    # num = e2.get()
    # if (num.isnumeric() == "false"):
    #     messagebox.showerror("Type Error", "Please enter the amount in $")

    e2.grid(row=2, column=1, sticky=W)
    Button(master, text='Quit', command=master.destroy, bd=2,
           fg="white",
           bg="#202225",
           font="Times",
           height=1,
           width=7,
           highlightcolor="purple",
           justify="right",
           padx=4,
           pady=8,
           relief="raised").grid(row=4, column=0, sticky=W, pady=6)

    Button(master, text='Input Data', command=show_entry_fields, bd=2,
           bg="#202225",
           fg="white",
           font="Times",
           height=1,
           width=7,
           highlightcolor="purple",
           justify="right",
           padx=4,
           pady=5,
           relief="raised").grid(row=4, column=1, sticky=W, pady=4)

    Button(master, text='Monthly report', command=monthly, bd=2,
           fg="white",
           bg="#202225",
           font="Times",
           height=1,
           width=11,
           highlightcolor="purple",
           justify="right",
           padx=4,
           pady=5,
           relief="raised").grid(row=4, column=2, sticky=W, pady=4)
    spacer1 = Label(master, text="", bg="#000000")
    spacer1.grid(row=12, column=0)

    status = Label(master, text="Expense Tracker", bd=1,
                   relief=SUNKEN, anchor=N, fg="#96DED1", bg="#28282B")
    status.grid(column=0, row=13, columnspan=3, sticky="WE")
    master.mainloop()


def billsplitter():
    root = Tk()
    root.title("BILL SPLITER")
    root["background"] = "#000000"
    root.resizable(False, False)

    def billsplit():
        f = int(q.get())/int(z.get())
        l = Label(root, text="Amount per person is :",
                  bg="#000000", fg="#FFFFFF")
        l.grid(row=2, column=0)
        l1 = Label(root, text=f, bg="#000000", fg="#FFFFFF")
        l1.grid(row=2, column=1)

    y = Label(root, text="Number of people", justify=LEFT,
              bg="#000000", fg="#FFFFFF").grid(sticky=W, row=0, column=0)
    x = Label(root, text="Total bill", bg="#000000",
              fg="#FFFFFF").grid(sticky=W, row=1, column=0)
    z = Entry(root, width=50, bg="#87CEEB", bd=2)
    q = Entry(root, width=50, bg="#87CEEB", bd=2)
    z.grid(row=0, column=1)
    q.grid(row=1, column=1, pady=2)

    t = Button(root, text='Input data', command=billsplit,
               bg="#50C878", fg="#1434A4").grid(row=3, column=1, pady=7)
    spacer1 = Label(root, text="", bg="#000000")
    spacer1.grid(row=12, column=0)

    status = Label(root, text="Bill Splitter", bd=1,
                   relief=SUNKEN, anchor=N, fg="#96DED1", bg="#28282B")
    status.grid(column=0, row=13, columnspan=7, sticky="WE")
    root.mainloop()


mlbtn = Button(frame, text="Money Ledger", font=("Tahoma"),
               bg="#50C878", fg="#1434A4", command=money)
mlbtn.grid(column=0, row=2, pady=25, ipadx=20, ipady=5)

expense_tracker_btn = Button(frame, text="Expense Tracker", font=(
    "Tahoma"), bg="#50C878", fg="#1434A4", command=expense)
expense_tracker_btn.grid(column=0, row=3, pady=25, ipadx=9, ipady=8)

billbtn = Button(frame, text="Bill Splitter", font=("Tahoma"),
                 bg="#50C878", fg="#1434A4", command=billsplitter)
billbtn.grid(column=0, row=4, pady=25, ipadx=33, ipady=5)


status = Label(root, text="Money Ledger", bd=1, relief=SUNKEN,
               anchor=N, fg="#96DED1", bg="#28282B")
status.grid(column=0, row=6, columnspan=3,pady=10, sticky=W+E)


root.mainloop()
