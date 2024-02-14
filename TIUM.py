from telegraph import Telegraph
from html_telegraph_poster.upload_images import upload_image
import os
import webbrowser
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as mb
from customtkinter import *
import tempfile, base64, zlib
from threading import Thread, Lock
import time

class App:
    def __init__(self):
        
        self.telegraph = Telegraph(access_token="021fbed97fd37d1f1a1e723801ec4e17c11a4c83997a153730330847a478")

        set_appearance_mode("system")
        self.root = CTk()
        self.root.title("Окно загрузчика")
        self.root.geometry("370x420+400+200")
        self.root.resizable(False,False)
        self.root.iconbitmap(self.nonicon())

        color1 = "#e07d25"
        color2 = "#ad601c"
        self.fg_color  = (color1, color1)
        self.hover_color  = (color2, color2)

        self.title = 'Поле "Название статьи" не может быть пустым'
        self.file = 'Неверное расположение файлов'
        self.file_emty = 'В папке отсутствуют изображения'

        self.top = CTkFrame(master=self.root, height=50, fg_color="transparent")
        self.input = CTkFrame(master=self.root, height=200, fg_color="transparent")
        self.setings = CTkFrame(master=self.root, height=50, fg_color="transparent")
        self.inputplus = CTkFrame(master=self.input, fg_color="transparent")
        
        self.name = CTkEntry(master=self.input, width=100, placeholder_text="Название статьи*")
        self.path = CTkEntry(master=self.inputplus, width=2000, placeholder_text="Разположение файлов*")
        self.autor = CTkEntry(master=self.input, placeholder_text="Автор")
        self.url_autor = CTkEntry(master=self.input, placeholder_text='Ссылка автора (вид: "http://" или "https://")')

        self.view = CTkButton(master=self.inputplus, text="Обзор", command=self.folder, width=70, fg_color=self.fg_color, hover_color=self.hover_color)
        self.upload = CTkButton(master=self.input, text="Загрузить статью", command=lambda: Thread(target=(self.noemty)).start(), fg_color=self.fg_color, hover_color=self.hover_color)

        self.pb = CTkProgressBar(master=self.input, orientation='horizontal', mode="determinate", progress_color=self.fg_color)

        self.error = CTkLabel(master=self.input, text="asdadad", text_color="#B71C1C")

    def run(self):
        self.draw_widgets()
        self.root.mainloop()
    
    def nonicon(self):
        ICON = zlib.decompress(base64.b64decode("eJxjYGAEQgEBBiDJwZDBysAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc="))
        _, ICON_PATH = tempfile.mkstemp()
        with open(ICON_PATH, "wb") as icon_file:
            icon_file.write(ICON)
        return ICON_PATH
    
    def draw_widgets(self):
        self.top.pack(fill=X, padx=30, pady=(30,0))
        self.input.pack(fill=X, padx=30)
        self.setings.pack(fill=X, padx=30, pady=(0,30))

        self.name.pack(side=TOP, fill=X, pady=(0,20))
        self.inputplus.pack(fill=X, pady=(0,20))
        self.view.pack(side=RIGHT)
        self.path.pack(side=LEFT, fill=X)
        self.autor.pack(fill=X, pady=(0,20))
        self.url_autor.pack(fill=X, pady=(0,20))
        self.upload.pack()
        self.pb.pack(pady=(30,0), fill=X)
        self.pb.set(0)

    def get_page(self):
        if self.autor.get():
            autor = self.autor.get()
        else:
            autor = "TIUM"
        if self.url_autor.get():
            url = self.url_autor.get()
        else:
            url = "https://github.com/Kolyanchan/Telegraph-Image-Uploader-for-manga"

        dr = str(self.path.get())
        files = []
        files += os.listdir(dr)
        to = 0
        content = " "
        self.pb.set(0)
        try:
            self.pb.configure(determinate_speed=50/len(files))
        except ZeroDivisionError:
            self.errors(self.file_emty)
        else:
            for i in files:
                a = "<img src="+str(upload_image(str(dr)+'/'+str(i)))+">"
                content+=a
                to+=1
                self.pb.step()
                self.pb.update()
                response = self.telegraph.create_page(
                    title = self.name.get(),
                    author_name=autor,
                    author_url=url,
                    html_content=content
                )
            res = response['url']
            response = StringVar()
            response.set(str(res))
            self.name.configure(textvariable=response)
            self.exit(res)

    def folder(self):
        self.path.delete(0, END)
        self.path.focus()
        ask_folder = filedialog.askdirectory()
        folder = StringVar()
        folder.set(str(ask_folder))    
        self.path.configure(textvariable=folder)

    def noemty(self):
        lock = Lock()
        if self.name.get() == "":
            self.errors(self.title)
            pass
        elif self.path.get() == '':
            self.errors(self.file)
            pass
        else:
            try:
                os.listdir(str(self.path.get()))
            except FileNotFoundError:
                self.errors(self.file)
            else:
                self.get_page()

    def errors(self, error_text):
        self.pb.pack_forget()
        self.error.configure(text=error_text)
        self.error.pack(side=TOP, pady=(15,0))
        self.root.update()
        time.sleep(3)
        self.error.pack_forget()
        self.pb.pack(pady=(30,0), fill=X)

    def exit(self, resp):    
        mb.showinfo("","Загрузка окончена")
        choice = mb.askyesno("ЗАГРУЗКА ЗАКОНЧЕНА", "Перейти на сайт и выйти из приложения?")
        if choice:
            webbrowser.open(resp, new=2)
            self.root.destroy()



if __name__ == "__main__":
    app = App()
    app.run()