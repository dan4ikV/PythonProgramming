import requests
from tkinter import *
from tkinter import font
import sqlite3
import json
import numpy as np
import ipaddress
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

conn = sqlite3.connect(r'names.db')

window = Tk()
currentCanvas = Canvas(window, width=300, height=200)
myLabel = Label(window, text='Waiting for actions...')
color = 'blue'

def create_table():
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS addresses_data ("
	"ip TEXT(15) NOT NULL,"
	"city TEXT(30) NOT NULL,"
	"country TEXT(30) NOT NULL,"
	"postal_code TEXT(10),"
    "PRIMARY KEY (ip)"
    ");")
    conn.commit()


def remove_current_layout():
    currentCanvas.forget()
    myLabel.config(text='Waiting for actions...')


def delete_all():
    cursor = conn.cursor()
    cursor.execute("DELETE FROM addresses_data;")
    conn.commit()
    myLabel.config(text='Database cleared')


def delete_all_page():
    global currentCanvas
    currentCanvas = Canvas(window, width=300, height=200)
    currentCanvas.pack()

    myLabel.config(text='After pressing the button all the database entries will be erased')
    btn_exit = Button(master=currentCanvas, text="Clear local database", command=lambda: delete_all())
    btn_exit.pack()


def delete_ip(ip):
    myLabel.config(text='processing...:')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM addresses_data where ip='{ip}';")
    conn.commit()
    myLabel.config(text=f"Data about \"{ip}\" was removed from the database")


def delete_ip_page():
    global currentCanvas
    currentCanvas = Canvas(window, width=300, height=200)
    currentCanvas.pack()

    myLabel.config(text='Enter ip to remove from database:')
    ip = StringVar()
    entry = Entry(master=currentCanvas, textvariable=ip)
    entry.pack()

    btn_exit = Button(master=currentCanvas, text="Remove", command=lambda: delete_ip(ip.get()))
    btn_exit.pack()


def add_ip(ip):
    global currentCanvas
    currentCanvas = Canvas(window, width=300, height=200)
    currentCanvas.pack()

    cursor = conn.cursor()
    myLabel.config(text='processing...:')
    url = f"https://ipinfo.io/{ip}/geo"
    response = requests.request("GET", url)
    myLabel.config(text=f"Info about \"{ip}\" added to the database")
    result = json.loads(response.text)

    print(result)

    ip_data = Label(master=currentCanvas, text=f'Data about {ip}')
    ip_data.pack()
    try:
        ip = result['ip']
    except(KeyError):
        myLabel.config(text=f"\"{ip}\" is an invalid ip address")
        return
    try:
        city = result['city']
    except(KeyError):
        city = 'Unknown'
    try:
        country = result['country']
    except(KeyError):
        country = 'Unknown'
    try:
        postal_code = result['postal']
    except(KeyError):
        postal_code = 'Unknown'
    syn = Label(master=currentCanvas, text=f'ip: {ip}, city: {city}, country: {country}, postal code: {postal_code}')
    syn.pack()
    print(f'INSERT into addresses_data (ip, city, country, postal_code) VALUES (\'{ip}\', \'{city}\', \'{country}\', \'{postal_code}\');')
    cursor.execute(f'INSERT into addresses_data (ip, city, country, postal_code) VALUES (\'{ip}\', \'{city}\', \'{country}\', \'{postal_code}\');')
    conn.commit()


def add_ip_data_page():
    global currentCanvas
    currentCanvas = Canvas(window, width=300, height=200)
    currentCanvas.pack()

    myLabel.config(text='Enter ip to add data about it to the database:')
    ip = StringVar()
    entry = Entry(master=currentCanvas, textvariable=ip)
    entry.pack()

    btn_exit = Button(master=currentCanvas, text="Add ip", command=lambda: [remove_current_layout(), btn_exit.pack_forget(), add_ip(ip.get())])
    btn_exit.pack()


def add_ip_range(range):
    global currentCanvas
    currentCanvas = Canvas(window, width=300, height=200)
    currentCanvas.pack()

    for ip in ipaddress.IPv4Network(range):
        cursor = conn.cursor()
        print(ip)
        myLabel.config(text='processing...:')
        url = f"https://ipinfo.io/{ip}/geo"
        response = requests.request("GET", url)
        myLabel.config(text=f"Info about \"{ip}\" added to the database")
        result = json.loads(response.text)
        print(result)
        ip_data = Label(master=currentCanvas, text=f'Data about {ip}')
        ip_data.pack()
        try:
            ip = result['ip']
        except(KeyError):
            myLabel.config(text=f"\"{ip}\" is an invalid ip address")
            return
        try:
            city = result['city']
        except(KeyError):
            city = 'Unknown'
        try:
            country = result['country']
        except(KeyError):
            country = 'Unknown'
        try:
            postal_code = result['postal']
        except(KeyError):
            postal_code = 'Unknown'
        syn = Label(master=currentCanvas, text=f'ip: {ip}, city: {city}, country: {country}, postal code: {postal_code}')
        syn.pack()
        print(
            f'INSERT into addresses_data (ip, city, country, postal_code) VALUES (\'{ip}\', \'{city}\', \'{country}\', \'{postal_code}\');')
        cursor.execute(
            f'INSERT into addresses_data (ip, city, country, postal_code) VALUES (\'{ip}\', \'{city}\', \'{country}\', \'{postal_code}\');')
        conn.commit()


def add_ip_range_page():
    global currentCanvas
    currentCanvas = Canvas(window, width=300, height=200)
    currentCanvas.pack()

    myLabel.config(text='Enter ip range via - in form "a.b.c.d-e.f.g.h" without spaces:')
    ip = StringVar()
    entry = Entry(master=currentCanvas, textvariable=ip)
    entry.pack()

    btn_exit = Button(master=currentCanvas, text="Add ip range", command=lambda: [remove_current_layout(), btn_exit.pack_forget(), add_ip_range(ip.get())])
    btn_exit.pack()


def show_stats_page():
    global currentCanvas
    currentCanvas = Canvas(window, width=300, height=200)
    currentCanvas.pack()

    cursor = conn.cursor()
    cursor.execute('SELECT city, count(ip) from addresses_data GROUP BY city ORDER BY count(ip);')
    for entry in cursor.fetchall():
        syn = Label(master=currentCanvas, text=f'City {entry[0]} has {entry[1]} ip addresses in the database')
        syn.pack()


def show_city_mean():
    global currentCanvas
    currentCanvas = Canvas(window, width=300, height=200)
    currentCanvas.pack()

    cursor = conn.cursor()
    cursor.execute(f'SELECT avg(number_of_ip) as avg_ip from (SELECT city, count(ip) as number_of_ip from addresses_data GROUP BY city ORDER BY count(ip));')
    syn = Label(master=currentCanvas, text=f'In average there is {str(*cursor.fetchone())} ip addresses per city in the database')
    syn.pack()


def show_city_mean_page():
    global currentCanvas
    currentCanvas = Canvas(window, width=300, height=200)
    currentCanvas.pack()

    btn_exit = Button(master=currentCanvas, text="Show ip stats", command=lambda: [remove_current_layout(), btn_exit.pack_forget(), show_city_mean()])
    btn_exit.pack()


def show_infographics():
    global currentCanvas
    currentCanvas = Canvas(window, width=300, height=200)
    currentCanvas.pack()

    cursor = conn.cursor()

    figure = plt.Figure(figsize=(10, 5))
    ax = figure.add_subplot(111)
    chart_type = FigureCanvasTkAgg(figure, currentCanvas)
    chart_type.get_tk_widget().pack()

    cursor.execute('SELECT city, count(ip) from addresses_data GROUP BY city ORDER BY count(ip);')
    temp = cursor.fetchall()

    x = list(list(zip(*temp))[0])
    y = np.array(list(zip(*temp))[1]).astype(int)
    ax.bar(x, y, color=color)
    ax.set_title('Number of ip\'s found per city')

def conf_font(font_set):
    def_font = font.nametofont("TkDefaultFont")
    def_font.configure(family=font_set)

def show_change_font():
    global currentCanvas
    currentCanvas = Canvas(window, width=300, height=200)
    currentCanvas.pack()

    variable = StringVar(window)
    variable.set("TkDefaultFont")  # default value

    w = OptionMenu(currentCanvas, variable, 'Times New Roman', 'Arial')
    w.pack()

    btn_exit = Button(master=currentCanvas, text="Set font", command=lambda: [conf_font(variable.get())])
    btn_exit.pack()


def change_color(col):
    global color
    color = col
    myLabel.config(text='color set')


def show_change_infographics_style():
    global currentCanvas
    currentCanvas = Canvas(window, width=300, height=200)
    currentCanvas.pack()

    myLabel.config(text='set the infographics color')
    variable = StringVar(window)
    variable.set("blue")  # default value

    w = OptionMenu(currentCanvas, variable, 'blue', 'red', 'orange')
    w.pack()

    btn_exit = Button(master=currentCanvas, text="Set color", command=lambda: change_color(variable.get()))
    btn_exit.pack()


def main_loop():
    window.minsize(400, 400)

    main_menu = Menu(window)
    window.config(menu=main_menu)

    delete_menu = Menu(main_menu, tearoff=0)
    delete_menu.add_command(label='Delete all entries', command=lambda: [remove_current_layout(), delete_all_page()])
    delete_menu.add_command(label='Delete single entry', command=lambda: [remove_current_layout(), delete_ip_page()])

    add_menu = Menu(main_menu, tearoff=0)
    add_menu.add_command(label='Add ip', command=lambda: [remove_current_layout(), add_ip_data_page()])
    add_menu.add_command(label='Add ip range', command=lambda: [remove_current_layout(), add_ip_range_page()])

    stats_menu = Menu(main_menu, tearoff=0)
    stats_menu.add_command(label='Text stats', command=lambda: [remove_current_layout(), show_stats_page()])
    stats_menu.add_command(label='Mean of ip\'s per city in the database', command=lambda: [remove_current_layout(), show_city_mean_page()])
    stats_menu.add_command(label='Infographic stats', command=lambda: [remove_current_layout(), show_infographics()])

    appearance_menu = Menu(main_menu, tearoff=0)
    appearance_menu.add_command(label='Application font', command=lambda: [remove_current_layout(), show_change_font()])
    appearance_menu.add_command(label='Infographic style', command=lambda: [remove_current_layout(), show_change_infographics_style()])

    main_menu.add_cascade(label="Delete", menu=delete_menu)
    main_menu.add_cascade(label="Add", menu=add_menu)
    main_menu.add_cascade(label="Statistics", menu=stats_menu)
    main_menu.add_cascade(label="Appearance", menu=appearance_menu)

    myLabel.pack()

    window.mainloop()

create_table()
main_loop()
