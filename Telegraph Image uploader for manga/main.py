from telegraph import Telegraph
from html_telegraph_poster.upload_images import upload_image
import os

telegraph = Telegraph()                                             # Инициализация модуля телеграф / Initialization of the Telegraph module


telegraph.create_account(short_name="TIUM_0.1")                     # Создание аккаунта телеграф для работы с ним / Creating a telegraph account to work with it

dr = input("Введите дерикторию : ")                                 # Указание дириктории страниц манги / Specifying the directory of manga pages
title1 = input("Введите название статьи: ")                         # Ввод названия статьи(главы) / Entering the title of the article (chapter)
autor = input("Введите имя автора (можно оставить пустым): ")
autor_url = input("Введите ссылку на автора (можно оставить пустым): ")

k = 0
img = " "                                                           # Начало статьи (начальный текст), при отсутствии не работает программа / The beginning of the article (the initial text), in the absence of the program does not work
files = []
files += os.listdir(dr)                                             # Создание массива с именами файлов указанной дириктории / Creating an array with the file names of the specified directory
print(files)
for i in files:
    k += 1
    prc = (k/len(files))*100
    a = "<img src="+str(upload_image(str(dr)+'/'+str(i)))+">"
    img += a                                                        # Генерация html кода для загрузки изображений / Generating html code for uploading images
    print('\rЗагруженно: {:.1f}%'.format(prc), end='')

if autor == False:
    autor = "Anonim"


response = telegraph.create_page(                       # Создание страницы телеграф / Creating a Telegraph page
    title = title1,
    author_name = autor,
    author_url = autor_url,
    html_content = img
)

print("\n","Готово: ",response['url'])                  # Получение ссылки на статью / Getting a link to an article
