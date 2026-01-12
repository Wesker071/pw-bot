import mss
import mss.tools
import os
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import pyautogui
import time
import tkinter as tk
from tkinter import ttk
from tkinter import Listbox, Scrollbar, END, MULTIPLE
import pyautogui
import pydirectinput
from difflib import SequenceMatcher
import cv2
import re
import numpy as np
import looting

come = True

path_object1 = r"C:\Users\qwe\Desktop\pw_bot2\coords\close.bmp"#закрыть окно координат
path_object2 = r"C:\Users\qwe\Desktop\pw_bot2\coords\coords.bmp"#значок координатного меню
path_object3 = r"C:\Users\qwe\Desktop\pw_bot2\coords\home.bmp"#2 раза кликнуть на заполненные координаты
path_object4 = r"C:\Users\qwe\Desktop\pw_bot2\coords\placeholder.bmp"#плейсхолдер для ввода координат
path_object5 = r"C:\Users\qwe\Desktop\pw_bot2\coords\remove_coords.bmp"#удалить старые координаты

path_object6 = r"C:\Users\qwe\Desktop\pw_bot2\coords\agr.bmp"#заагрить моба
path_object7 = r"C:\Users\qwe\Desktop\pw_bot2\coords\flowers_buff.bmp"#бафнуться на цветы


array_paths = [path_object1]

monitor1 = {"top": 57, "left": 837, "width": 140, "height": 14}#для поиска мобов
namefile1 = 'screen.png'#для поиска мобов

monitor4 = {"top": 381, "left": 47, "width": 50, "height": 16}#для хп
namefile4 = 'xp1.png'#для хп

monitor5 = {"top": 381, "left": 140, "width": 50, "height": 16}#для mp
namefile5 = 'mp1.png'#для маны

monitor6 = {"top": 112, "left": 820, "width": 180, "height": 21}#для защиты от магии
namefile6 = 'ismagic.png'#для защиты от магии

monitor7 = {"top": 62, "left": 1550, "width": 42, "height": 13}#для координат
namefile7 = 'coords.png'#координаты


array_text_immun_magic = ['иленная магическая защи']

#Изменяемые параметры со временем:
length_xp = 4
length_mp = 4
XP = 2067
MP = 1699

coords1 = [616, 711]#координаты безопасной локации
coords_for_while = [coords1[0]-1,coords1[0],coords1[0]+1,coords1[1]-1,coords1[1],coords1[1]+1]#разброс координат безопасной локации (спасибо криворуким разрабам игры)
##################################


################################################################################################
#Функция которая возвращает % (0-100) о совпадении
def find_best_match_percentage(text, word_array):
    """
    Находит наиболее похожее слово из массива и процент его сходства с заданным текстом.

    Args:
        text: Исходный текст для сравнения.
        word_array: Массив слов для поиска наилучшего соответствия.

    Returns:
        Кортеж (наилучшее_совпадение, процент_совпадения).
        Если массив пуст, возвращает (None, 0).
    """

    if not word_array:
        return None, 0  # Обработка пустого массива

    best_match = None
    best_ratio = 0

    for word in word_array:
        ratio = SequenceMatcher(None, text.lower(), word.lower()).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = word

    return best_ratio * 100
################################################################################################

def remove_text_before_bracket(text):

  try:
    index = text.index(']')  # Находим индекс первого вхождения символа "]"
    return text[index+1:]    # Возвращаем подстроку, начиная со следующего символа после "]"
  except ValueError:
    # Если символ "]" не найден, возвращаем исходную строку
    return text
  
def add_unique_text(array, text):
  if text not in array:
    array.append(text)
    return True
  else:
    return False

class Bot:
    def __init__(self, number_kreeps, master, app):
        self.number_kreeps = number_kreeps#количество мобов которых мы будем искать
        self.is_searching = False
        self.mob_name = ''
        self.mob_list = []
        self.master = master
        self.app = app
        self.xp = XP
        self.mp = MP
        self.isHill = False
        self.count = 0
        self.isRange = False
        self.my_coords = []
        self.isFly = False

    def go_home(self):
        looting.looting([path_object2])#открываем меню координат
        looting.looting([path_object4])#наводим на плейсхолдер координат

        for _ in range(8):
            pydirectinput.keyDown('backspace')#удаляем координаты старые

        for number in coords1:
            for i in str(number):
                pydirectinput.press(str(i))
            pydirectinput.press('space')

        pydirectinput.press('enter')

        for number in coords1:
            for i in str(number):
                pydirectinput.press(str(i))
            pydirectinput.press('space')

        pydirectinput.press('enter')
        looting.looting([path_object3])#2 раза кликнуть на заполненные координаты
        pydirectinput.doubleClick()
        looting.looting([path_object5])#удаляем все точки маршрута
        pydirectinput.press('enter')
        looting.looting([path_object1])#закрываем окно координат





    def screen(self,monitor,namefile,k):
        output_folder = r"C:\Users\qwe\Desktop\pw_bot2"
        # Создайте папку, если она не существует
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        try:
            with mss.mss() as sct:
                # Получите информацию о мониторах
                #monitor = {"top": 47, "left": 820, "width": 180, "height": 35}
                # Сделайте скриншот
                sct_img = sct.grab(monitor)
                # Создайте имя файла
                filename = os.path.join(output_folder, namefile) # или используйте time.strftime("%Y%m%d_%H%M%S.png") для уникальных имен
                # Сохраните скриншот
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)
                #print(f"Скриншот сохранен в: {filename}")
                image_path = rf"C:\Users\qwe\Desktop\pw_bot2\{namefile}"
                img = Image.open(image_path)
                 # 4. Предобработка изображения для улучшения OCR (самая важная часть!)
                # --------------------------------------------------------------------------
                # a. Преобразование в оттенки серого (упрощает обработку)
                img = img.convert('L')
                # b. Изменение размера (увеличение улучшает детализацию для Tesseract)
                width, height = img.size
                new_width = width * k  # Увеличение в 3 раза
                new_height = height * k
                img = img.resize((new_width, new_height), Image.LANCZOS)  # LANCZOS для лучшего качества
                # c. Повышение контрастности (делает текст более четким)
                enhancer = ImageEnhance.Contrast(img)
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(1.1)  # Увеличение контрастности в 2 раза (экспериментируйте)
                # d. Удаление шума (медианный фильтр, если есть мелкий шум)
                img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=180, threshold=3))
                # e. Дополнительная фильтрация (резкость)
                img.save(os.path.join(output_folder, namefile))
        except mss.exception.ScreenShotError as e:
            print(f"Ошибка при создании скриншота: {e}.  Убедитесь, что у вас есть права доступа к экрану (например, предоставьте разрешение в настройках системы).")
    def scan_text(self,namefile):
        image_path = rf"C:\Users\qwe\Desktop\pw_bot2\{namefile}"
        text = ''
        try:
            # 3. Откройте изображение с помощью Pillow
            img = Image.open(image_path)
            # Настройка конфигурации Tesseract для максимальной точности
            config = ('-l rus --oem 3 --psm 7')  # Попробуйте разные PSM, начиная с 6
            text = pytesseract.image_to_string(img, config=config)
            #self.mob_name = remove_text_before_bracket(text.rstrip())#удаляем все после ] и обновляем имя найденного моба и удаляем \n
            return text
            
        except FileNotFoundError:
            print(f"Ошибка: Файл '{image_path}' не найден.")
        except Exception as e:
            print(f"Ошибка: {e}")

    def create_mob_list(self):

        for _ in range(10):
            self.screen(monitor1,namefile1,3)
            self.mob_name = remove_text_before_bracket(self.scan_text(namefile1).rstrip())
            add_unique_text(self.mob_list,self.mob_name)#добавляем найденного моба в список если он не повторяется
            print(self.mob_list)
        self.show_list()

        self.change_coords()#обновим свои координаты

    def remove_mob_list(self):
     self.mob_list = []
     self.show_list()

    def change_coords(self):
        self.screen(monitor7,namefile7,4)
        try:
            text = self.scan_text(namefile7).rstrip()
            my_coords = text.split(",")
            my_coords = [int(num.strip()) for num in my_coords]
            self.my_coords = my_coords
        except:
            self.my_coords = [111,111]#если эта тварина не сможет распознать текст - то заместо ошибки пусть хоть эту дичь вернет

    def is_immun_magic(self):#если моб с иммунитетом от магии
       self.screen(monitor6,namefile6,4) 
       text = self.scan_text(namefile6).rstrip()
       return text

    def show_list(self): 
                        
            listbox = Listbox(self.master, selectmode=MULTIPLE)

            listbox.place(x=50, y=50, width=300, height=100)  # Размещаем с использованием place

            for mob in self.mob_list:
                listbox.insert(END, mob)

    def back_to_search_mob(self):

        global come
        come = True

        self.still_alive()
        pydirectinput.press('f1')#подбираем лут на всякий случай
        time.sleep(0.5)
        pydirectinput.press('f1')#подбираем лут на всякий случай
        time.sleep(0.5)

        xp_now, mp_now = self.watch_xp_mp()

        if(mp_now/self.mp<0.7):#если мана закончилась, то юзнуть гармонику
            if(xp_now/self.xp < 0.85):
                pyautogui.press('f4')#если мало хп при свапе маны и хп , то похилиться
                pyautogui.press('8')#ну и раз уж закончилась мана - юзнуть кларетку
            else:
                pydirectinput.press('f6')#гармоника
                self.still_alive()
                pydirectinput.press('7')
                time.sleep(4)

        pydirectinput.press('tab') 

    def fight(self):
        global come

        self.still_alive()#проверяем что вот вот не сдохнем

        self.screen(monitor1,namefile1,3)
        self.mob_name = remove_text_before_bracket(self.scan_text(namefile1).rstrip())

        if(find_best_match_percentage(self.mob_name,self.mob_list)>=70):

            if(come == True):#если бьем первый раз - подбежать
                looting.looting([path_object6])#заагрить моба петом
                self.still_alive()
                looting.looting([path_object7])#бафнуться на цветы
                time.sleep(2)
                pydirectinput.press('f3')
                self.still_alive()
                pydirectinput.press('f3')
                pydirectinput.press('f1')
                time.sleep(4)
                self.still_alive()
                pydirectinput.press('6')#подхилить махнатого
                
            pydirectinput.press('2')
            self.still_alive()
            pydirectinput.press('f3')

            time.sleep(1)
            self.still_alive()

            pydirectinput.press('1')
            self.still_alive()
            pydirectinput.press('f3')

            pydirectinput.press('6')#подхилить махнатого

            if(come == True):
                pydirectinput.press('6')#подхилить махнатого
                come = False
                self.still_alive()

            self.still_alive()

        else:
            #подбираем лут
            ########################
            pydirectinput.press('f1')
            time.sleep(1)
            pydirectinput.press('f1')
            time.sleep(1)
            pydirectinput.press('f1')
            time.sleep(1)
            self.still_alive()
            ########################

            #хилим медведя
            ########################
            pydirectinput.press('6')
            time.sleep(3)
            self.still_alive()
            ########################

            come = True
            self.still_alive()
            pydirectinput.press('tab')
            

    def hunt(self):
        global come
        self.fight()
        self.master.after_idle(self.schedule_hunt) # Планируем следующий hunt

    def schedule_hunt(self): # отдельная функция планировщик.
        self.master.after(500, self.hunt)


    def start_hunt(self): #Переименовываем stop_hunt в start_hunt
        self.app.isHunt = True #Используем ссылку на app для доступа к переменной
        self.hunt() #Запускаем охоту

    def stop_hunt(self):
        self.app.isHunt = False #Используем ссылку на app для доступа к переменной
        xp_now, mp_now = self.watch_xp_mp()

        time.sleep(2)
        self.still_alive()

    def checkbox_changed(bot):
        if var1.get() == 1:
            bot.isRange = True#Чекбокс отмечен
        else:
            bot.isRange = False#Чекбокс снят

    def checkbox_changed2(bot):
        if var2.get() == 1:
            bot.isFly = True#Чекбокс отмечен
        else:
            bot.isFly = False#Чекбокс снят

    def still_alive(self):

        global come

        xp_now, mp_now = self.watch_xp_mp()

        if(xp_now/self.xp > 0.65 and xp_now/self.xp < 0.85):
            pydirectinput.press('9')

        if(mp_now/self.mp > 0.35 and mp_now/self.mp < 0.55):
            pydirectinput.press('8')

        if(self.isFly and xp_now/self.xp <= 0.55):
            pydirectinput.press('f4')#подхил
            time.sleep(0.1)
            pydirectinput.press('f2')#отозвать полет
            time.sleep(8)#упасть
            pyautogui.press('7')#подхил со скила
            time.sleep(4)
            pydirectinput.press('f4')#подхил
            pyautogui.keyDown('space')#подъем к поыерхности воды
            time.sleep(3)
            pyautogui.keyUp('space')#остановка подъема
            pydirectinput.press('f2')#вызвать полет
            time.sleep(1)
            pyautogui.keyDown('space')#подъем к мобам
            time.sleep(20)
            pyautogui.keyUp('space')#остановка подъема
            time.sleep(1)
            pydirectinput.press('3')#вызвать осу
            time.sleep(3)
            pydirectinput.press('6')#подхилим осу
            pydirectinput.press('tab')

        if(xp_now/self.xp <= 0.65):
            pydirectinput.press('f4')#подхил
            pydirectinput.press('space')
            time.sleep(0.7)
            pydirectinput.press('space')
            time.sleep(0.5)
            pydirectinput.press('f2')#вызвать полет
            pyautogui.keyDown('space')#подъем
            time.sleep(5)
            pyautogui.keyUp('space')#остановка подъема
            pyautogui.keyDown('space')#подъем
            time.sleep(5)
            pyautogui.keyUp('space')#остановка подъема

            #если бьем ренджевиков или опасных тварин то отслеживать свои координаты
            if(self.isRange):
                self.change_coords()#обновляем свои координаты
            pyautogui.press('f4')#подхил

            pyautogui.press('f5')#выйти из образа лисы
            time.sleep(7)
            pyautogui.press('7')#подхил со скила
            time.sleep(7)
            pyautogui.press('f5')#войти в образ лисы
            time.sleep(3)

            if(xp_now/self.xp <= 0.75):
                pydirectinput.press('f4')#подхил

            #если выбран режим ренджевик - значит нужно отдыхать в защищенном месте 
            if(self.isRange):
                self.go_home()#вбиваем коорды и пиздуем на базу
                while (self.my_coords[0] not in coords_for_while and self.my_coords[1] not in coords_for_while):
                    self.change_coords()
                    print('пока не прилетели ',self.my_coords)
                    time.sleep(5)
                print('прилетели домой')

            #падаем -> призываем мишу -> хилим
            pydirectinput.press('f2')
            time.sleep(8)
            pydirectinput.press('5')#призвать медведя
            time.sleep(5)
            pydirectinput.press('6')
            come = True
            pydirectinput.press('tab')
            time.sleep(2)#иногда не хватает времени после подхила

    def watch_xp_mp(self):
            try:
                self.screen(monitor4,namefile4,5)
                self.screen(monitor5,namefile5,5)
                text_xp = int(re.sub(r'[^a-zA-Z0-9]', '', remove_text_before_bracket(self.scan_text(namefile4).rstrip()))[:len(str(XP))])
                text_mp = int(re.sub(r'[^a-zA-Z0-9]', '', remove_text_before_bracket(self.scan_text(namefile5).rstrip()))[:len(str(MP))])
               
                #Если хп или мана считанные каким то образом больше чем пороговое изначальное - то разделить его на 10 (убрать цифру справа)
                if(text_xp>XP*2):
                    text_xp = text_xp/10

                #Если хп или мана считанные каким то образом больше чем пороговое изначальное - то разделить его на 10 (убрать цифру справа)
                if(text_mp>MP*2):
                    print('делю ману на 10 ',text_mp)
                    text_mp = text_mp/10

                return (text_xp,text_mp)
            
            except:
                return (XP,MP)#всегда меняется
        
class App:
   def __init__(self,master):
      self.master = master
      self.bot = Bot(20, master,self)
      self.isHunt = False
      master.title("Бот для афк-фарма")
      master.geometry("600x800")
      self.isRange = False

      self.add_button = ttk.Button(master, text="Добавление моба в моб-лист", command=self.bot.create_mob_list)
      self.add_button.place(x=40, y=750)

      self.clear_button = ttk.Button(master, text="Очистить список", command=self.bot.remove_mob_list)
      self.clear_button.place(x=450, y=750)

      self.hanter = ttk.Button(master, text="Бить мобов", command=self.bot.start_hunt)
      self.hanter.place(x=300, y=750)

      self.stop_hunt = ttk.Button(master, text="Стоп", command=self.bot.stop_hunt)
      self.stop_hunt.place(x=0, y=700)

      checkbox = ttk.Checkbutton(root, text="Ренджевик", variable=var1, command=self.bot.checkbox_changed)
      checkbox.pack(pady=5)

      checkbox2 = ttk.Checkbutton(root, text="На полёте", variable=var2, command=self.bot.checkbox_changed2)
      checkbox2.pack(pady=5)

root = tk.Tk()
var1 = tk.IntVar()# для чекбокса
var2 = tk.IntVar()# для чекбокса
app = App(root)
root.mainloop()







    








