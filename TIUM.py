from telegraph import Telegraph
from html_telegraph_poster.upload_images import upload_image
import os
import webbrowser
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as mb
from customtkinter import *
import tempfile, base64, zlib


ICON = zlib.decompress(base64.b64decode("eJxjYGAEQgEBBiDJwZDBysAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc="))
_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, "wb") as icon_file:
    icon_file.write(ICON)

telegraph = Telegraph(access_token='021fbed97fd37d1f1a1e723801ec4e17c11a4c83997a153730330847a478')

set_appearance_mode("system")
app = CTk()
app.title("Окно загрузчика")
app.geometry("370x400+400+200")
#app.resizable(False,False)
app.iconbitmap(default=ICON_PATH)

color1 = "#e07d25"
color2 = "#ad601c"

def run():
    app.mainloop()

def folder():
    e2.delete(0, END)
    e2.focus()
    ask_folder = filedialog.askdirectory()
    folder = StringVar()
    folder.set(str(ask_folder))    
    e2.configure(textvariable=folder)

def noemty():
    if e1.get() == "":
        error(title)
    else:
        l2.configure(text = "")
        get_page()

def error(error_text):
    l2.configure(text = error_text)

def get_page():
    if e3.get():
        autor = e3.get()
    else:
        autor = "TIUM"
    if e4.get():
        url = e4.get()
    else:
        url = "https://github.com/Kolyanchan/Telegraph-Image-Uploader-for-manga"

    dr = str(e2.get())
    files = []
    try:
        files += os.listdir(dr)
    except FileNotFoundError:
        l2.configure(text = path)
    to = 0
    content = " "
    pb.set(0)
    pb.configure(determinate_speed=50/len(files))
    for i in files:
        a = "<img src="+str(upload_image(str(dr)+'/'+str(i)))+">"
        content+=a
        to+=1
        pb.step()
        pb.update()
        response = telegraph.create_page(
            title = e1.get(),
            author_name=autor,
            author_url=url,
            html_content=content
        )
    res = response['url']
    response = StringVar()
    response.set(str(res))
    e1.configure(textvariable=response)
    exit(res)

def exit(resp):    
    mb.showinfo("","Загрузка окончена")
    choice = mb.askyesno("ЗАГРУЗКА ЗАКОНЧЕНА", "Перейти на сайт и выйти из приложения?")
    if choice:
        webbrowser.open(resp, new=2)
        app.destroy()
    
    

l1 = CTkLabel(master=app, text="Загрузка изображений в статьи telegraph", font=('Century Gothic', 20))
l1.pack(anchor="n", pady=30)

frame1 = CTkFrame(master=app)
frame1.pack(side=TOP, fill=X, padx=30)
frame1.configure(fg_color="transparent")

e1 = CTkEntry(master=frame1, width=100, placeholder_text="Название статьи*")
e1.pack(side=TOP, fill=X, pady=(0,20))

frame2 = CTkFrame(master=frame1)
frame2.pack(side=TOP, pady=(0,20))
frame2.configure(fg_color="transparent")


b1 = CTkButton(master=frame2, text="Обзор", width=70, command=folder, fg_color=(color1, color1), hover_color=(color2, color2) )
b1.pack(side=RIGHT)

e2 = CTkEntry(master=frame2, width=2000, placeholder_text="Разположение файлов*")
e2.pack(side=LEFT, fill=X)

frame3 = CTkFrame(master=frame1)
frame3.pack(side=TOP, pady=(0,20), fill = X)
frame3.configure(fg_color="transparent")

e3 = CTkEntry(master=frame3, width=100, placeholder_text="Автор")
e3.pack(side=TOP, fill=X, pady=(0,20))

e4 = CTkEntry(master=frame3, width=100, placeholder_text='Ссылка автора (вид: "http://" или "https://")')
e4.pack(side=TOP, fill=X, pady=(0,20))

b2 = CTkButton(master=frame1, text="Загрузить статью", command=noemty, fg_color=(color1, color1), hover_color=(color2, color2))
b2.pack(side=TOP)

pb = CTkProgressBar(master=frame1, orientation='horizontal', mode="determinate", progress_color=(color1, color1))
pb.pack(side=TOP, pady=(30,0), fill=X)
pb.set(0)

l2 = CTkLabel(master=app, text="", text_color="#B71C1C")
l2.pack(side=TOP, pady=(50,0))

title = 'Поле "Название статьи" не может быть пустым'
path = 'Неверное расположение файлов'

run()