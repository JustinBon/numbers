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

def bestdim(n):
    dim = (0,0,0)
    while True:
        max_dim = int(np.ceil(n**0.5))
        
        for i in range(1,max_dim+1):
            if i**2/n > 1:
                break
            if n % i == 0 and i**2/n > 0.5 and i**2/n > dim[2]:
                dim=(i,int(n/i),i**2/n)
        if dim[2] != 0:
            return dim
        n += 1

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

def frequency(n):
    freq=0
    todaysnumbers = readdatabase()
    for i in todaysnumbers.keys():
        if todaysnumbers[i]==n:
            freq+=1
    return freq

def makecollage():
    for i in range(1,11):
        cols, rows , _ = bestdim(frequency(i))
        thumb_width = int(1920/cols)
        thumb_height = int(1080/rows)
        new_im= Image.new("RGB",(1920,1080))
        ims = []
        x, y, j = 0, 0, 0
        for file in os.listdir(PATH0+"\\"+numbers[i-1]+"\\frames\\"):
            im=Image.open(PATH0+"\\"+numbers[i-1]+"\\frames\\"+file)
            ims.append(im.resize((thumb_width, thumb_height)))
        print(len(ims))
        for k in range(len(ims)):
            x = thumb_width*(int(np.floor(k / rows)))
            y = thumb_height* (k%rows)
            new_im.paste(ims[j], (x, y))
            j+=1
        new_im.save(PATH0+"\\..\\static\\collage\\"+str(i)+".jpg")

downloadnewvids()
findframes()
findnumbers()
exceptions()
moveframes()
makecollage()
os.system('cleanup.bat')