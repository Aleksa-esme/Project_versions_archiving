from tkinter import *
from tkinter import messagebox as mb
from tkinter.ttk import Combobox as cb
from tkinter import filedialog as fd
from os import path, walk, chdir, curdir
from zipfile import ZipFile
from datetime import datetime

ask_path = ''
copy_path = ''

def check_path_func():
    global ask_path
    ask_path = fd.askdirectory()
    from_path.set(ask_path)
    return ask_path

def copy_path_func():
    global copy_path
    copy_path = fd.askdirectory()
    to_path.set(copy_path)
    return copy_path

def check_files():
    now = datetime.now()
    archive_name = ((str(now.strftime("%d-%m-%Y_%H_%M"))) + '.zip')
    new_path = chdir(ask_path)
    new_path = curdir
    file_paths = []
    old_time_file = {}
    new_file_paths = {}

    if path.exists(path.join(new_path,'times.txt')):
        with open('times.txt', 'r') as read_f:
            for i in read_f.readlines():
                key,val = i.strip().split(':')
                old_time_file[key] = val
        for address, dirs, files in walk(new_path):
            for dir_name in dirs:
                dir_path = path.join(address, dir_name)
                dir_time = path.getmtime(dir_path)
                file_paths.append(dir_path)
                new_file_paths.update({dir_path:f'{dir_time}'})
                for file_name in files:
                    if file_name != 'times.txt':
                        #if os.path.normpath(item.filename) != os.path.normpath(file):
                        file_path = path.join(address, file_name)
                        file_time = path.getmtime(file_path)
                        if file_name not in file_paths:
                            file_paths.append(file_path)
                            new_file_paths.update({file_path:f'{file_time}'})
        unmatched_item = set(old_time_file.items()) ^ set(new_file_paths.items())
        l = len(unmatched_item)
        if l == 0:
            mb.showinfo('Сообщение', 'Новых файлов не обнаружено')
        else:
            with ZipFile(path.join(copy_path, archive_name), 'w') as zip:
                for file in file_paths:
                    zip.write(file)
            mb.showinfo('Сообщение', 'Файлы скопированы')

    else:
        for address, dirs, files in walk(new_path):
            for dir_name in dirs:
                dir_path = path.join(address, dir_name)
                dir_time = path.getmtime(dir_path)
                file_paths.append(dir_path)
                with open('times.txt', 'a') as f:
                    f.write(f'{dir_path}:{dir_time}\n')
                for file_name in files:
                    file_path = path.join(address, file_name)
                    file_paths.append(file_path)
                    file_time = path.getmtime(file_path)
                    with open('times.txt', 'a') as f:
                        f.write(f'{file_path}:{file_time}\n')

        with ZipFile(path.join(copy_path,archive_name), 'w') as zip:
            for file in file_paths:
                zip.write(file)
        mb.showinfo('Сообщение', 'Файлы скопированы')

window = Tk()
window.title('Super Puper Copy Program ')
window.geometry('550x250')

lbl_check = Label(window, text="Путь для проверки", font=("Arial Bold", 10))
lbl_check.grid(column=0, row=0)
from_path = StringVar()
lbl_path = Label(master=window, textvariable=from_path)
lbl_path.grid(column=1, row=1)

btn_choose = Button(window, text="Выбрать", bg="grey", fg="white", command=check_path_func)
btn_choose.grid(column=0, row=1)

lbl_copy = Label(window, text="Путь для копирования", font=("Arial Bold", 10))
lbl_copy.grid(column=0, row=2)
to_path = StringVar()
lbl_path_copy = Label(master=window, textvariable=to_path)
lbl_path_copy.grid(column=1, row=3)
btn_choose = Button(window, text="Выбрать", bg="grey", fg="white", command=copy_path_func)
btn_choose.grid(column=0, row=3)

lbl = Label(window, text="Выбор форматов", font=("Arial Bold", 10))
lbl.grid(column=0, row=4)

all_state = BooleanVar()
all_state.set(True)
all_f = Checkbutton(window, text='Все форматы', var=all_state)
all_f.grid(column=3, row=5)

avi_state = BooleanVar()
avi_state.set(True)
avi = Checkbutton(window, text='AVI', var=avi_state)
avi.grid(column=0, row=5)

txt_state = BooleanVar()
txt_state.set(True)
txt = Checkbutton(window, text='TXT', var=txt_state)
txt.grid(column=0, row=6)

jpg_state = BooleanVar()
jpg_state.set(True)
jpg = Checkbutton(window, text='JPG', var=jpg_state)
jpg.grid(column=1, row=5)

png_state = BooleanVar()
png_state.set(True)
png = Checkbutton(window, text='PNG', var=txt_state)
png.grid(column=1, row=6)

level_text = Label(window, text="Выбор уровней копирования", font=("Arial Bold", 10))
level_text.grid(column=0, row=7)
copy_level = cb(window)
copy_level['values'] = (1, 2, 3)
copy_level.current(0)
copy_level.grid(column=1, row=7)

btn_check = Button(window, text="Проверить", bg="grey", fg="white", command=check_files)
btn_check.grid(column=0, row=8)


window.mainloop()