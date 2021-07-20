import sqlite3
from sqlite3 import Error
from PIL import Image
import os
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
database = sqlite3.connect('recepies.sqlite')
handMain = database.cursor()
cls()
print('\n\n')
print("\t\tWe Have Assumed That You Have All The Basic MASALAS In Your KITCHEN ()")
print("\n\n")
handMain.execute('SELECT typee, ingred FROM ingr')
for row in handMain:
    for element in row:
        print('   ',element)
    print(' ')
print(' Enter the ingredients you have: \n (Make sure they are seperated by commas)')
itemm = input("\n\t")
lst = itemm.split(',')
newList = []
for lsitem in lst:
    newList.append(lsitem.strip().capitalize())
cls()    
print(7*'\n')
print('\tYour selected items are:\n')
print("\t" , *newList,sep='\n\t')   
ingredient = handMain.execute('SELECT ingre FROM Table1')
matchedList = []
track=0
for newRow in ingredient:
    for line in newRow:
        iteList = []
        newls = line.split(",")
        for ite in newls:
            iteList.append(ite.strip().capitalize())
        diffList = list(set(newList)-set(iteList))+list(set(iteList)-set(newList))
        track+=1
        flag = 0
        if(set(iteList).issubset(set(newList))):
            flag=1
        if flag == 1:
            matchedList.append(track)
print("\n")
if len(matchedList) == 0:print("    Please Try Again, No recepie is Found in our database with your current selection. \n   Thank You!\n\n")
elif len(matchedList) == 1 :print("    This is the recepie You can try:")
else:print("    These are the recepies You can try:\n")
srNo = 0
handMain.execute('DELETE FROM runtime')
if len(matchedList) > 0 :
    for tracks in matchedList:
        identifier = handMain.execute('SELECT code,food,ingre FROM Table1 WHERE num = ?',(tracks, ))
        xx = identifier.fetchone()
        srNo+=1
        print("    ", srNo,'. ' , xx[1])
        print("             Ingredients for this selection are:")
        print("             ",xx[2],"\n")
        handMain.execute('''INSERT INTO runtime(code,item) VALUES(?,?)''',(xx[0],xx[1]))
        database.commit()
if len(matchedList)>0:
    sItem=input("\n\n\tEnter Your Choice:")
    cls()
    try:
        selection = handMain.execute('SELECT code FROM runtime WHERE id = ?',(sItem,))
        cook =  selection.fetchone()
        itee=cook[0]
        folder = "rec/" + itee + ".txt"
        img = "rec/images/" + itee + ".jpg"
        print("\n\n\n\n\t\t\t HAPPY COOKING! \n\t\t\tYour Recipe for:\n\n")
        with open(folder) as f:
            for line in f:print("\t\t"+f.read()+7*"\n")
        try:
            im = Image.open(img)
            im.show()
        except:
            print("Please Install PIL to view the image of Your Dish\n Use Command 'pip install PIL' " + 3*"\n")
    except:
        print("Invalid Selection!\n\n\n")