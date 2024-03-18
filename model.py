import numpy as np
from xgboost import XGBClassifier
import sqlite3
import pickle
from sklearn.model_selection import train_test_split
from gtts import gTTS
from pygame import mixer_music
import io
from random import randint
##############################################################

# Aby program działał należy zainstalować wszelkie biblioteki których używa program!
# Program został napisany przez Mateusza Błaszczyk
# poczta gmail: mateuszblaszczyk36@gmail.com
# numer telefonu: +48 723 871 171
# discord: ._.kitler._.


##############################################################



# W tej funkcji wyciągame dane do nauki dla modelu ręki pierwszej 
def fetch_data():
    conn = sqlite3.connect('baza.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT f1,f2,f3,f4,f5,x1,y1,z1,key FROM dane ORDER BY key ASC")
    rows = cursor.fetchall()
    conn.close()
    palce = []
    x = []
    y = []
    z = []
    keyy = []
    for r in rows:
        palce.append(r[0:5])
        x.append(list(eval(r[5])))
        y.append(list(eval(r[6])))
        z.append(list(eval(r[7])))
        keyy.append(int(r[8]))
    return palce, x, y, z, keyy 



# W tej funkcji wyciągame dane do nauki dla modelu ręki drugiej
def fetch_data2():
    conn2 = sqlite3.connect('baza2.sqlite')
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT f11,f22,f33,f44,f55,x2,y2,z2,key FROM dane ORDER BY key ASC")
    rows2 = cursor2.fetchall()
    conn2.close()
    palce2 = []
    x2 = []
    y2 = []
    z2 = []
    keyy = []
    for r in rows2:
        palce2.append(r[0:5])
        x2.append(list(eval(r[5])))
        y2.append(list(eval(r[6])))
        z2.append(list(eval(r[7])))
        keyy.append(int(r[8]))
    return palce2, x2, y2, z2, keyy



# Ta funkcja wyciąga dane do predykcji
def fetch_predict():
    conn3 = sqlite3.connect('key.sqlite')
    cursor3 = conn3.cursor()
    cursor3.execute("SELECT text,dictkey FROM dane")
    rows = cursor3.fetchall()
    conn3.close()
    t = {}
    for r in rows:
        t[tuple(eval(r[1]))] = (r[0])
    return t

# Model do nauki gestów dla pierwszej ręki
def model():
    _, x, y, z, t = fetch_data()
    model=XGBClassifier(eta=0.1,min_child_weight=2,colsample_bytree=0.9,reg_alpha=0.1,reg_lambda=0.8, max_depth=8, gamma=0)
    xx = np.concatenate((x,y), axis=1)
    yy = np.concatenate((y,z), axis=1)
    zz = np.concatenate((z,x), axis=1)
    features = np.concatenate((xx, yy, zz), axis=1)
    X_train, x_test, y_train, y_test = train_test_split(features, t, test_size=0.1)
    model.fit(X_train,y_train)
    xx = np.concatenate((x,y), axis=1)
    yy = np.concatenate((y,z), axis=1)
    zz = np.concatenate((z,x), axis=1)
    features = np.concatenate((xx, yy, zz), axis=1)
    with open("model.pkl","wb") as f:
        pickle.dump((model),f)


# Model do nauki gestów dla drugiej ręki
def model2():
    _, x, y, z, t = fetch_data()
    model2=XGBClassifier(eta=0.1,min_child_weight=2,colsample_bytree=0.9,reg_alpha=0.1,reg_lambda=0.8, max_depth=8, gamma=0)
    xx = np.concatenate((x,y), axis=1)
    yy = np.concatenate((y,z), axis=1)
    zz = np.concatenate((z,x), axis=1)
    features = np.concatenate((xx, yy, zz), axis=1)
    X_train, x_test, y_train, y_test = train_test_split(features, t, test_size=0.1)
    model2.fit(X_train,y_train)
    xx = np.concatenate((x,y), axis=1)
    yy = np.concatenate((y,z), axis=1)
    zz = np.concatenate((z,x), axis=1)
    features = np.concatenate((xx, yy, zz), axis=1)
    with open("model2.pkl","wb") as f:
        pickle.dump((model2),f)



# Funkcja odpowiedzialna za tworzenie predykcji z obu modeli
def predict(x,y,z,xx,yy,zz, model, model2):
    xy = np.array((x,y))
    xz = np.array((x,z))
    zy = np.array((y,z))
    features = np.concatenate((xy,xz,zy), axis=0)
    features = np.reshape(features,(1,6000))
    prediction = model.predict(features)
    xy1 = np.array((xx,yy))
    xz1 = np.array((xx,zz))
    zy1 = np.array((yy,zz))
    features1 = np.concatenate((xy1,xz1,zy1), axis=0)
    features1 = np.reshape(features1,(1,6000))
    prediction2 = model2.predict(features1)
    print(prediction,prediction2)
    t=fetch_predict()
    buffer = io.BytesIO()
    print(t[(prediction[0],prediction2[0])])
    t=gTTS(t[(prediction[0],prediction2[0])], lang='pl')
    t.write_to_fp(buffer)
    buffer.seek(0)
    mixer_music.load(buffer)
    mixer_music.play(1)


    
# Tu wpisujemy funkcje
if __name__ == "__main__":
    model()
    model2()
    