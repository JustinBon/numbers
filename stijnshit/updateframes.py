import os
import shutil
import datetime
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np

PATH0 = os.getcwd()
numbers= ["ones","twos","threes","fours","fives","sixes","sevens","eights","nines","tens"]
number = {1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight",9:"nine",10:"10"}
startdate = datetime.date(2020,8,17)
print(PATH0)
with open("last checked.txt") as f:
    lastchecked = f.read()
    print(lastchecked)

#exceptions
def exceptions():
    todaysnumbers=np.load('todaysnumbers.npy',allow_pickle=True).item()
    todaysnumbers[0]=8
    todaysnumbers[2]=9
    todaysnumbers[30]=9
    todaysnumbers[51]=6
    todaysnumbers[6]=9
    todaysnumbers[99]=9
    todaysnumbers[256]=1
    np.save('todaysnumbers', todaysnumbers)

def date2number(file):
    date_name = [int(i) for i in file.split(' ')[-1].split('-')[0].split('_')]
    date = datetime.date(date_name[2]+2000,date_name[0],date_name[1])
    return str((date - startdate).days)

def downloadnewvids():
    with open("last checked.txt") as f:
        lastchecked = f.read()
    os.system('newvid.bat '+lastchecked)
    for file in os.listdir(PATH0+"\\vids"):
        if int(date2number(file))+1 > int(lastchecked):
            lastchecked = str(int(date2number(file))+1)
    with open("last checked.txt","w") as f:
        f.write(lastchecked)

def findframes():
    for file in os.listdir(PATH0+"\\vids"):
        print(file)
        count = 900
        if date2number(file)+"_frame.jpg" not in os.listdir(PATH0+"\\frames"):
            vidcap = cv2.VideoCapture(PATH0 + '\\vids\\' + file)
            vidcap.set(cv2.CAP_PROP_POS_FRAMES,count)
            success,image = vidcap.read()
            color = image.mean()
            while success:
                if color > 10 and image.mean() < 1:
                    breakpoint = count - 5
                    vidcap.set(cv2.CAP_PROP_POS_FRAMES,breakpoint)
                    success, image = vidcap.read()
                    print(PATH0 + '\\frames\\' + date2number(file) +"_frame.jpg")
                    cv2.imwrite(PATH0 + '\\frames\\' + date2number(file) +"_frame.jpg", image)
                    break 
                color = image.mean()
                success, image = vidcap.read()
                count += 1
            
def findnumbers():
    todaysnumbers=np.load('todaysnumbers.npy',allow_pickle=True).item()
    for file in os.listdir(PATH0+"\\subs"):
        with open(PATH0+"\\subs\\"+file) as f:
            subs = f.read()[-200:-100]
            found = False
            for i in range(1,10):
                n = number[i]
                if subs.find(n) != -1:
                    todaysnumber = i
                    found = True
            if found == False:
                todaysnumber = 10
        todaysnumbers[int(date2number(file))]=todaysnumber
    np.save('todaysnumbers', todaysnumbers)
    
def moveframes():
    todaysnumbers=np.load('todaysnumbers.npy',allow_pickle=True).item()
    for file in os.listdir(PATH0+"\\frames"):
        daynumb = int(file.split('_')[0])
        todaysnumber = todaysnumbers[daynumb]
        shutil.move(PATH0+"\\frames\\"+file, PATH0+"\\"+numbers[todaysnumber-1]+"\\frames\\"+file)

def readdatabase():
    return np.load('todaysnumbers.npy',allow_pickle=True).item()

downloadnewvids()
# findframes()
findnumbers()
exceptions()
moveframes()
os.system('cleanup.bat')