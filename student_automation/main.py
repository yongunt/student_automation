from tkinter import *
from tkinter import ttk
import sqlite3

win = Tk()
win.title("Öğrenci Formu")
win.resizable(False, False)

# Labels
Label(win, text="Adı: ", font=("Times New Roman", 14, "normal")).grid(row=0, column=0)
Label(win, text="Soyadı: ", font=("Times New Roman", 14, "normal")).grid(row=1, column=0)
Label(win, text="Öğrenci No: ", font=("Times New Roman", 14, "normal")).grid(row=2, column=0)

# Entries
name = Entry(win, font=("Times New Roman", 14, "normal"))
surname = Entry(win, font=("Times New Roman", 14, "normal"))
no = Entry(win, font=("Times New Roman", 14, "normal"))

name.grid(row=0, column=1)
surname.grid(row=1, column=1)
no.grid(row=2, column=1)


def clear_entries():
    for widget in win.winfo_children():
        if widget.winfo_class() == 'Entry':
            widget.delete(0, END)
    
    clear_table()
    create_table()


# Functions
def save_infos():
    con = sqlite3.connect('student.db')
    cursor = con.cursor()
    
    cursor.execute("SELECT * FROM Students")
    students = cursor.fetchall()
    existing_students = [s[3] for s in students]

    if no.get() not in existing_students and (no.get()).isdigit():
        sqlite_insert_query = f"""INSERT INTO Students
                                    (Ad, Soyad, No) 
                                    VALUES
                                    ("{name.get().capitalize()}", "{surname.get().capitalize()}", "{no.get()}")"""

        cursor.execute(sqlite_insert_query)
        con.commit()
        
        clear_entries()
        clear_table()
        create_table()

    cursor.close()
    con.close()


def delete_student(No:str):
    con = sqlite3.connect('student.db')
    cursor = con.cursor()

    cursor.execute(f""" DELETE FROM Students WHERE No = "{No}" """)
    con.commit()

    cursor.close()
    con.close()

    clear_table()
    create_table()


def update_student(ID:int, name:str, surname:str, no:str):
    win3 = Tk()
    win3.geometry("350x200")
    win3.title("Öğrenci Formu")

    # Labels
    Label(win3, text="Adı: ", font=("Times New Roman", 14, "normal")).grid(row=0, column=0)
    Label(win3, text="Soyadı: ", font=("Times New Roman", 14, "normal")).grid(row=1, column=0)
    Label(win3, text="Öğrenci No: ", font=("Times New Roman", 14, "normal")).grid(row=2, column=0)

    # Entries
    name2 = Entry(win3, font=("Times New Roman", 14, "normal"))
    surname2 = Entry(win3, font=("Times New Roman", 14, "normal"))
    no2 = Entry(win3, font=("Times New Roman", 14, "normal"))

    name2.insert(0, name)
    surname2.insert(0, surname)
    no2.insert(0, no)

    name2.grid(row=0, column=1)
    surname2.grid(row=1, column=1)
    no2.grid(row=2, column=1)


    def update():
        con = sqlite3.connect('student.db')
        cursor = con.cursor()
        
        cursor.execute("SELECT * FROM Students")
        students = cursor.fetchall()
        existing_students = [s[3] for s in students if s[3] != no]

        if no2.get() not in existing_students and (no2.get()).isdigit():
            sqlite_update_query = f"""UPDATE Students
                                            SET Ad = "{name2.get().capitalize()}", 
                                                Soyad = "{surname2.get().capitalize()}", 
                                                No = "{no2.get()}"
                                            WHERE STUDENTID = {str(ID)}
                                            """

            cursor.execute(sqlite_update_query)
            con.commit()
            
            win3.destroy()

            clear_table()
            create_table()

        cursor.close()
        con.close()


    #Button
    Button(win3, text="GÜNCELLE", command=update).grid(row=3, column=1, columnspan=2)

    win3.mainloop()


def clear_table():
    for widget in win.winfo_children()[11:]:    
        widget.destroy()


def create_table(students=None):
    if students is None:
        con = sqlite3.connect('student.db')
        cursor = con.cursor()
    
        cursor.execute("SELECT * FROM Students")
        students = cursor.fetchall()

        cursor.close()
        con.close()

        height = len(students)
        width = 4
    else:
        if students != []:
            height = len(students)
            width = 4
        else:
            height = 0
            width = 0
    
    r = 7
    headers = ["Ad", "Soyad", "Okul No"] 
    for i in range(len(headers)):
        b = Entry(win)
        b.insert(0, headers[i])
        b.configure(font=("Times New Roman", 15, "bold"), fg="red")
        b.configure(state="readonly")
        b.grid(row=r-1, column=i)

    for i in range(height):
        for j in range(1, width):
            if j == 3:
                Button(win, text="SİL", command=lambda c=i: delete_student(No=students[c][3])).grid(row=i+r, column=3)
                Button(win, text="DÜZENLE", command=lambda c=i: update_student(ID=students[c][0], name=students[c][1], surname=students[c][2], no=students[c][3])).grid(row=i+r, column=4)
                b = Entry(win)
                b.insert(0, str(students[i][j]))
                b.configure(font=("Times New Roman", 15, "bold"))
                b.configure(state="readonly")
                b.grid(row=i+r, column=j-1)
            else:
                b = Entry(win)
                b.insert(0, str(students[i][j]))
                b.configure(font=("Times New Roman", 15, "bold"))
                b.configure(state="readonly")
                b.grid(row=i+r, column=j-1)


# Searching
search_val = StringVar()
combo_val = StringVar()


def onComboChange(e):
    for widget in win.winfo_children():
        if widget.winfo_class() == 'Entry':
            widget.delete(0, END)
    
    clear_table()
    create_table()


def OnEntryChange(e):
    bar = search_val.get()
    comb = combo_val.get()
    if bar != "":
        con = sqlite3.connect('student.db')
        cursor = con.cursor()

        cursor.execute(f''' SELECT * FROM Students WHERE {comb} LIKE "{bar.capitalize()}%" ''')
        students = cursor.fetchall()

        clear_table()
        create_table(students=students)

        cursor.close()
        con.close()
    else:
        clear_table()
        create_table()
    

Label(win, text="Öğrenci Ara: ", font=("Times New Roman", 12, "normal")).grid(row=5, column=0)

search_ent = Entry(win, width=40, textvariable=search_val, font=("Times New Roman", 15, "bold"))
search_ent.bind("<KeyRelease>", OnEntryChange)
search_ent.grid(row=5, column=1, columnspan=2, pady=25)

combo = ttk.Combobox(win, values=["Ad", "Soyad", "No"], state="readonly", textvariable=combo_val)
combo.current(0)
combo.bind('<<ComboboxSelected>>', onComboChange)
combo.grid(row=5, column=3, columnspan=10)

# Buttons
Button(win, text="Kaydet", font=("Times New Roman", 10, "normal"), command=save_infos).grid(row=3, column=1)
Button(win, text="Temizle", font=("Times New Roman", 10, "normal"), command=clear_entries).grid(row=4, column=1)

create_table()

win.mainloop()