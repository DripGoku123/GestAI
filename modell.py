import pygame
import model
from time import sleep
import sqlite3
import pickle
from sklearn.decomposition import PCA
from scipy.interpolate import CubicSpline
import numpy as np
pygame.init()
w = pygame.display.set_mode((800,800))

##############################################################

# Aby program działał należy zainstalować wszelkie biblioteki których używa program!
# Program został napisany przez Mateusza Błaszczyk
# poczta gmail: mateuszblaszczyk36@gmail.com
# numer telefonu: +48 723 871 171
# discord: ._.kitler._.


##############################################################
# Tworzenie wszystkich tabeli do baz danych
conn = sqlite3.connect('baza.sqlite')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS dane (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        f1 INTEGER,
        f2 INTEGER,
        f3 INTEGER,
        f4 INTEGER,
        f5 INTEGER,
        x1 TEXT,
        y1 TEXT,
        z1 TEXT,
        key INTEGER)
''')

conn2 = sqlite3.connect('baza2.sqlite')
cursor2 = conn2.cursor()
cursor2.execute('''
    CREATE TABLE IF NOT EXISTS dane (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        f11 INTEGER,
        f22 INTEGER,
        f33 INTEGER,
        f44 INTEGER,
        f55 INTEGER,
        x2 TEXT,
        y2 TEXT,
        z2 TEXT,
        key INTEGER)
''')

conn3 = sqlite3.connect('key.sqlite')
cursor3 = conn3.cursor()
cursor3.execute('''
    CREATE TABLE IF NOT EXISTS dane (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        dictkey TEXT,
        hand1 TEXT,
        hand2 TEXT)
''')
##############################################################



# Funkcja do zapisywania danych do nauki gestów dla obu rąk
def insert_data(data_tuple, data_tuple2):
    cursor.execute("INSERT INTO dane (f1, f2, f3, f4, f5, x1, y1, z1, key) VALUES (?, ?, ?,?, ?, ?, ?, ?, ?)",
                   data_tuple)
    conn.commit()
    cursor2.execute("INSERT INTO dane (f11, f22, f33, f44, f55, x2, y2, z2, key) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?)",
                   data_tuple2)
    conn2.commit()



# Funkcja używana przez dicctt() do zapisywania 4 danych do predykcji
def insert_dict(conn,dictt):
   cursor3.execute("INSERT INTO dane (text, dictkey, hand1, hand2) VALUES (?,?,?,?)", dictt)
   conn3.commit()



#Funkcja odpowiedzialna za podanie danych do predykcji
# a : jest to zmienna touple. Ogólnie model uczy się jako klasyfikator czy zwraca on liczbę int w liście po której się uczył np [1]
#     lecz ze względu na to iż zwraca on predykcje z dwóch rąk to zwraca przykładowo [0] [1]. Aby funkcja fetch_predict() działała dobrze 
#     należy tu wpisać przykładowo (1,1) gdzie te liczby to predykcje pierwszej i drugiej ręki

# aa : jest to text który ma zwracać predykcja
   
# aaa : należy tu wpisywać dane zgiętych palców w tuple. Oryginalnie w naszym projekcie 0 oznacza niezgięty palec a 1 zgięty. Zapisujemy
#       dane w przykładowo taki sposób (0,0,0,1,1)
   
# aaaa : należy tu również wpisywać dane zgiętych palców w tuple drugiej ręki. Oryginalnie w naszym projekcie 0 oznacza niezgięty 
#        palec a 1 zgięty. Zapisujemy dane w przykładowo taki sposób (0,0,0,1,1)
def dicctt():
   pygame.quit()
   T=True
   while T:
      a = input("dictkey >>> ")
      if a == "???":
         exit()
      aa = input("text >>> ")
      aaa = input("palce hand1 >>>")
      aaaa = input("palce hand2 >>>")
      print()
      insert_dict(conn,(aa,a,aaa,aaaa))



# Funkcja stworzona do zapisywania danych x,y,z do baz danych baza.sqlite i baza2.sqlite
def main(key, key2):
    T = True
    esc_pressed = False
    l = []
    xx = []
    yy = []
    pygame.display.set_caption("Tryb zapisu danych r1 (zapisuj se indexy i slowa na kartce)")
    w.fill((0,0,0))
    while T:
      for e in pygame.event.get():
         if e.type == pygame.QUIT:
            exit()
      x,y = pygame.mouse.get_pos()
      k = pygame.key.get_pressed()
      if k[pygame.K_1]:
         esc_pressed=True
         sleep(0.2)

      if len(xx)==1000:
         sleep(0.2)
         mainn(xx,yy,l,key,key2)
      if esc_pressed:
         l.append([x,y])
         xx.append(x)
         yy.append(y)
      if k[pygame.K_2]:
         aaa = input("podaj klucz klucz >>>")
         aa = input("podaj klucz2 liczbe >>>")
         main(aaa,aa)
      if k[pygame.K_4]:
         sleep(0.2)
         main2()
      for ll in l:
         pygame.draw.rect(w,(255,0,0) , (ll[0],ll[1],1,1))
      pygame.display.update()




def mainn(xx,yy,l,key,key2):
   T = True
   esc_pressed = False
   xx1 = []
   yy1 = []
   print(len(xx))
   pygame.display.set_caption("Tryb zapisu danych r2 (zapisuj se indexy i slowa na kartce)")
   w.fill((0,0,0))
   while T:
      for e in pygame.event.get():
         if e.type == pygame.QUIT:
            exit()
      x,y = pygame.mouse.get_pos()
      k = pygame.key.get_pressed()
      if k[pygame.K_1]:
         esc_pressed=True
         sleep(0.2)
      if esc_pressed:
         l.append([x,y])
         xx1.append(x)
         yy1.append(y)
      
      if len(xx1) == 1000:
            esc_pressed=False
            
            insert_data((1,1,1,1,1,str(xx),str(yy),str(yy), key), (1,1,1,1,1,str(xx1),str(yy1),str(yy1),key2))
            print("Zapisano!")
            main(key, key2)
      for ll in l:
            pygame.draw.rect(w,(255,0,0) , (ll[0],ll[1],1,1))
      pygame.display.update()

# Funkcja stworzona tylko po to aby testować predykcje modelu
def main2():
   with open("model.pkl", "rb") as f:
        model2 = pickle.load(f)
   with open("model2.pkl", "rb") as f:
        model4 = pickle.load(f)
   T = True
   l = []
   xx = []
   yy = []
   zz = []
   xx1 = []
   yy1 = []
   zz1 = []
   set = 1
   esc_pressed=False
   pygame.display.set_caption("Tryb testowania modelu")
   w.fill((0,0,0))
   while T:
      for e in pygame.event.get():
         if e.type == pygame.QUIT:
            exit()
      if set==1:
         x,y = pygame.mouse.get_pos()
         k = pygame.key.get_pressed()
         if k[pygame.K_1]:
            esc_pressed=True
            sleep(0.1)
         if len(xx) == 1000:
            esc_pressed=False
            set=None
         if esc_pressed:
            l.append([x,y])
            xx.append(x)
            yy.append(y)
            zz.append(y)            
         if k[pygame.K_4]:
            sleep(0.2)
            aaa = input("podaj klucz klucz >>>")
            aa = input("podaj klucz2 liczbe >>>")
            main(aaa,aa)
         for ll in l:
            pygame.draw.rect(w,(255,0,0) , (ll[0],ll[1],1,1))
      else:
         w.fill((0,0,0))
         x,y = pygame.mouse.get_pos()
         k = pygame.key.get_pressed()
         if k[pygame.K_1]:
               esc_pressed=True
               sleep(0.1)
         if esc_pressed:
            l.append([x,y])
            xx1.append(x)
            yy1.append(y)
            zz1.append(y)
         if len(zz1) == 1000:
            esc_pressed=False
            model.predict(xx,yy,zz,xx1,yy1,zz1,model2, model4)
            main2()
         for ll in l:
            pygame.draw.rect(w,(255,0,0) , (ll[0],ll[1],1,1))
      pygame.display.update()


def delete_table(n):
   cursor.execute("DELETE FROM dane WHERE key = %i;"%(n))
   cursor2.execute("DELETE FROM dane WHERE key = %i;"%(n))
   conn.commit()
   conn2.commit()
   print("usunięto")
# Tu należy wpisywać funkcje których chcemy użyć
if __name__ == "__main__":
   aa = input("key1>>>")
   aaa = input("key2>>>")
   main(aa,aaa)   
    