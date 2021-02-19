import sqlite3
import os
import pyperclip
import tkinter as tk
from tkinter import messagebox,scrolledtext,font
from tkinter.ttk import *
from imdb import add_movies,delete_movies,show_details
import fontawesome as fa

def copy(cont):
    k= cont.get("1.0","end-1c")
    pyperclip.copy(k)

def add_to_list():
    global movies
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute("SELECT NAME FROM MOVIES")
    k = c.fetchall()
    for i in k:
        movies.append(i[0])
    conn.commit()
    conn.close()


def add():
    mos = entry_box.get().split(",")
    add_movies(mos)
    for i in mos:
        movies.append(i.strip().upper())


def delete():
    mos = entry_box.get().split(",")
    delete_movies(mos)
    for i in mos:
        if (i=="Select A Movie"):
            continue
        movies.remove(i.strip().upper())


def show():
    query = movies_box.get()
    if (query=="Select A Movie"):
        messagebox.showerror(title="Select a movie!!", message="Please select a movie from the combobox and try again!!")
    else:
        det = show_details(query)
        if det==0:
            return
        else:
            info = tk.Toplevel()
            title= query+" : Info"
            info.title(title)
            info.geometry("300x260")
            if ("nt" == os.name):
                info.iconbitmap("./icon.ico")
            info.resizable(0, 0)
            canvas = tk.Canvas(info, width=300, height=260, bg="#070769")
            canvas.pack(fill=tk.BOTH)
            content = scrolledtext.ScrolledText(
            info, wrap=tk.WORD, height=12, width=27, font="Arial 12", relief="groove", borderwidth=0)
            content.place(x=20, y=20)
            cont = '''Name: {}
Year: {}
Star: {}
Ratings: {}
Watchtime: {}
Release Date and Location: {}
Genre: {}
Summary: {}
            '''.format(det[0],det[1],det[2],det[3],det[4],det[5],det[6],det[7])
            content.insert (tk.END, cont)
            cpy = tk.Button(info,text =fa.icons['copy'], font="Arial 20",
                command=lambda: copy(content), activebackground='#343434',background="#ffffff", activeforeground='#ffffff', borderwidth=0)
            cpy.place (x=220,y=22)
            

def entered1(event):
    add.configure(
        bg="#343434",
        fg="#ffffff",
    )


def left1(event):
    add.configure(
        bg="#ffffff",
        fg="#000000",
    )


def entered2(event):
    delete.configure(
        bg="#343434",
        fg="#ffffff",
    )


def left2(event):
    delete.configure(
        bg="#ffffff",
        fg="#000000",
    )


def entered3(event):
    show.configure(
        bg="#343434",
        fg="#ffffff",
    )


def left3(event):
    show.configure(
        bg="#ffffff",
        fg="#000000",
    )


root = tk.Tk()
root.title("IMDB Stats")
root.geometry("400x400")
root.resizable(0, 0)
if ("nt" == os.name):
    root.iconbitmap("./icon.ico")
movies = ["Select A Movie"]
add_to_list()
canvas = tk.Canvas(root, width=400, height=400, bg="#070769")
canvas.create_text(200, 30, fill="white", font="Arial 16 bold",
                   text="Add Movies & Find Their Info!")
canvas.create_text(205, 100, fill="white", font="Arial 14",
                   text="Add/Remove Movie/(s) (for multiple movies, \nseparate them using a comma ',')")
entry_box = tk.Entry(root, width=33, font="Arial 14",
                 relief="groove", borderwidth=0)
entry_box.place(x=17, y=140)
add = tk.Button(root, width=21, text="Add Movie/(s)", font="Arial 10 bold", command=add,
                activebackground='#343434', activeforeground='#ffffff', borderwidth=0)
add.place(x=17, y=180)
delete = tk.Button(root, width=21, text="Remove Movie/(s)", font="Arial 10 bold",
                command=delete, activebackground='#343434', activeforeground='#ffffff', borderwidth=0)
delete.place(x=208, y=180)
movies_box = Combobox(root, values=movies, width=49, font="Arial 10", state="readonly",
                      postcommand=lambda: movies_box.configure(values=movies))
movies_box.current(0)
movies_box.place(x=17, y=240)
show = tk.Button(root, width=45, text="Show Details", font="Arial 10 bold",
                command=show, activebackground='#343434', activeforeground='#ffffff', borderwidth=0)
show.place(x=17, y=280)
canvas.pack(fill=tk.BOTH)
add.bind("<Enter>", entered1)
add.bind("<Leave>", left1)
delete.bind("<Enter>", entered2)
delete.bind("<Leave>", left2)
show.bind("<Enter>", entered3)
show.bind("<Leave>", left3)
root.mainloop()
