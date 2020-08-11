#PLEASE DO NOT MESS AROUND IF U DON'T KNOW WHAT YOU ARE DOING
#YOU WILL BE HANDLING FILES OUTSIDE THE CWD, DATA MAY BE LOST IF YOU DO NOT KNOW WHAT YOU ARE DOING!
#==HAT-TRICK==#

#importing libraries which may be required...
import os, sys, time, threading, multiprocessing
#import zipfile, shutil
from ftplib import FTP
import ftplib
from configparser import ConfigParser
import getpass
import archivetools as arch
import misctools as misc

#made an ftp object to connect to
ftp = FTP()

#made a games configparser object to read specific profiles for games from games.ini
games = ConfigParser()
games.read('games.ini')
gamelist = games.sections()

#made a config configparser object to read configuration for ftp in config.ini
config = ConfigParser()
config.read('config.ini')

#made a welcome object to be referenced when trying connection to ftp
welcome = ''

#getting curent username for use in directories
user = getpass.getuser()
maindir = 'C:\\Users\\'+user

#if u don't get this then u r unqualified to be here
def ftpconn(host,port=21, usr='anonymous', pswd='',dir='/'):
    ftp.connect(host,port)
    ftp.login(user=usr, passwd=pswd)
    return(ftp.getwelcome())

#ftp is the ftp object created earlier
#filename (str) is of the file which is to be got
#local (open file object) is where it's data is saved.
def ftpget(ftp, filename, local):
    file = open(local, 'wb')
    ftp.retrbinary('RETR ' + filename, file.write, 1024)
    file.close()
    return

#ftp is the ftp object created earlier
#filename is the filename u r sending to the ftp
def ftpsend(ftp, filename):
    ftp.storbinary('STOR '+filename, open(filename, 'rb'))
    return

def fin():
    if ftp.voidcmd("NOOP"):
        ftp.close()
        sys.exit()
    else:
        sys.exit()

def pathparser(gamename):
    extpath = games[gamename]['extpath']
    path = maindir+'\\'+extpath
    return path

def envsetup():
    if 'saves' in ftp.nlst():
        ftp.cwd('saves')
    else:
        ftp.mkd('saves')
        ftp.cwd('saves')

def backup(ftp, gamename):
    if gamename in ftp.nlst():
        name = misc.namer(gamename)
        choice = input('''Enter custom save name y/n: ''')
        if choice == 'n':
            time = name[-10:]
            ftp.cwd(gamename)
            ftp.mkd(time)
            ftp.cwd(time)
        elif choice == 'y':
            savename = input("Enter name for save (Unique, else old one deleted/Overwrited): ")
            ftp.cwd(gamename)
            if savename in ftp.nlst():
                ftp.cwd(savename)
                for filename in ftp.nlst():
                    ftp.delete(filename)
                ftp.cwd('..')
                ftp.rmd(savename)
            ftp.mkd(savename)
            ftp.cwd(savename)
        zipped = name+'.zip'
        arch.zipdir(str(os.getcwd()+'\\'+'\\'+name), pathparser(gamename))
        ftpsend(ftp, zipped)
        os.remove(zipped)
        ftp.cwd('/'+'saves')
        return
#===CENTURY ==#
    else:
        ftp.mkd(gamename)
        backup(ftp, gamename)

def load(ftp, gamename, customsavename = None):
    if gamename in ftp.nlst():
        ftp.cwd(gamename)
        if customsavename:
            if customsavename in ftp.nlst():
                ftp.cwd(customsavename)
                files = ftp.nlst()
                for save in files:
                    ftpget(ftp, save, save)
                ftp.cwd('/'+'saves')
                return
            else:
                print("Error custom save does NOT exist... please resume from start after confirming name!")
                return
        else:
            print("Custom save name not provided!")
            while True:
                choice = input('''
Enter choice:
1) Load latest one available (Recommended)
2) Browse yourself
3) Go back to view other options
''')
                if choice == '1':
                    dmod = 0
                    kingfolder = ''
                    for folder in ftp.nlst():
                        mod = int(ftp.voidcmd(f"MDTM %s" %folder)[-14:])
                        if mod >= dmod:
                            dmod = mod
                            kingfolder = folder
                        else:
                            continue
                    if kingfolder != '':
                        ftp.cwd(kingfolder)
                        files = ftp.nlst()
                        for file in files:
                            ftpget(ftp,file,file)
                            break
                        ftp.cwd('/'+'saves')
                        return
                    else:
                        print("SCHMARRTY!!! FOLDER WAS EMPTY!!! LULL")
                        return
                        
                if choice == '2':
                    print("This option is under construction!")
                    return
                if choice == '3':
                    return
                else:
                    print("Invalid choice! please enter a number!")
    else:
        print("Saves of given game do NOT EXIST (DA FOQ) please resume from start after confirming name!")
        return

def dispatcher():
    count = 0
    for filename in os.listdir():
        if '.zip' in filename:
            count+=1
            gamename = misc.rev(filename[-15::-1])
            wannabepath = pathparser(gamename)
            arch.extract(filename, wannabepath)
            os.remove(filename)
            print("Dispatch Success!!")
            return
    if count == 0:
        print("No saves in directory!")
        return
def interface():
    while True:
        mainchoice = input('''
    1) Send NOOP to server
    2) Game save/load menu
    3) Exit (Safely)
    ''')
        if mainchoice == '1':
            print(ftp.voidcmd("NOOP"))
        elif mainchoice == '2':
            while True:
                choice = input('''
    1) See the profiled games that can be saved from this device: 
    2) Load a save game and put it in the correct dir
    3) Main menu
    ''')
                if choice == '1':
                    while True:
                        for i in range(0,len(gamelist)):
                            print(f"{i+1}) {gamelist[i]} ")
                        print(f"{len(gamelist)+1}) Exit")
                        savechoice = misc.typeensure(input("Enter number of the thing you want to backup: "), int)
                        if savechoice in range(1,len(gamelist)+1):
                            backup(ftp,gamelist[savechoice-1])
                        elif savechoice == len(gamelist)+1:
#==DOUBLE-CENTURY==#
                            break
                        else:
                            print("Invalid Choice!")
                if choice == '2':
                    while True:
                        for i in range(0,len(gamelist)):
                            print(f"{i+1}) {gamelist[i]} ")
                        print(f"{len(gamelist)+1}) Exit")
                        savechoice = misc.typeensure(input("Enter number of the thing you want to load: "), int)
                        if savechoice == len(gamelist)+1:
                                break
                        elif savechoice in range(1,len(gamelist)):
                            while True:
                                qsavename = input("If you had a savename and you remember it and you need it press 'y' otherwise 'n': ")
                                if qsavename == 'y': 
                                    savename = input("Enter savename: ")
                                    load(ftp,gamelist[savechoice-1], savename)
                                    dispatcher()
                                    print("Restored")
                                    break
                                elif qsavename == 'n':
                                    load(ftp,gamelist[savechoice])
                                    dispatcher()
                                    print("Restored")
                                    break
                                else:
                                    print("Invalid choice! Enter y/n")
                            else:
                                print("Invalid Choice!")
                if choice == '3':
                    break
                else:
                    print("Invalid choice!")
        elif mainchoice == '3':
            fin()
        else:
            print("Invalid Choice!")

def configconn():
    global welcome
    global ftplib
    while False == bool(welcome):
        try:
            welcome = ftpconn(config['FTP']['host'], misc.typeensure(config['FTP']['port'], int), config['FTP']['user'], config['FTP']['password'])
            return welcome
        except ftplib.all_errors as e:
            print("An error occured in the connection...")
            print("Sleeping 5 seconds then retrying... \n")
            time.sleep(5)
            configconn()

configconn()
print(welcome+'\n')
envsetup()
interface()

