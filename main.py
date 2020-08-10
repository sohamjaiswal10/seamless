#PLEASE DO NOT MESS AROUND IF U DON'T KNOW WHAT YOU ARE DOING
#YOU WILL BE HANDLING FILES OUTSIDE THE CWD, DATA ON THE 
#MAY BE LOST IF YOU DO NOT KNOW WHAT YOU ARE DOING!

#importing libraries which may be required...
import os, sys, time, threading, multiprocessing
import zipfile, shutil
from ftplib import FTP
from configparser import ConfigParser
import getpass

#made an ftp object to connect to
ftp = FTP()

#made an openlist list to keep track of open files, so that program closes safely
#without corrupting anything
openlist=[]

#made a games configparser object to read specific profiles for games from games.ini
games = ConfigParser()
games.read('games.ini')
gamelist = games.sections()

#made a config configparser object to read configuration for ftp in config.ini
config = ConfigParser()
config.read('config.ini')

#getting curent username for use in directories
user = getpass.getuser()
maindir = 'C:\\Users\\'+user

#direct is the directory, out is the file
def zipdir(out, direct): 
    shutil.make_archive(out, 'zip', direct)

#to unzip saves, path is where the zip is, direct is where to save zip
def extract(path, direct): 
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(direct)

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

#ftp is the ftp object created earlier
#filename is the filename u r sending to the ftp
def ftpsend(ftp, filename):
    ftp.storbinary('STOR '+filename, open(filename, 'rb'))

def typeensure(var,typ):
    try:
        typ = typ(var)
    except:
        print("Sorry the type cannot be converted to what it's supposed to be... try again")
        var = input(f"Enter the thing which will be convertible to %s type" %str(typ))
        typeensure(var, typ)
    finally:
        return(typ)

def fin():
    if ftp.voidcmd("NOOP") and openlist[0]:
        ftp.close()
        for file in openlist:
            file.close()
        sys.exit()
    elif not ftp.voidcmd("NOOP") and openlist[0]:
        for file in openlist:
            file.close()
        sys.exit()
    elif ftp.voidcmd("NOOP") and not openlist[0]:
        ftp.close()
        sys.exit()
    else:
        sys.exit()

def pathparser(extpath):
    path = maindir+'\\'+extpath
    return path

def namer(gamename):
    name = gamename + str(time.time())[0:10]
    return name

def backup(ftp, gamename):
    if gamename in ftp.nlst():
        name = namer(gamename)
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
                ftp.rmd(savename)
            ftp.mkd(savename)
            ftp.cwd(savename)
        zipped = name+'.zip'
        zipdir(str(os.getcwd()+'\\'+'\\'+name), pathparser(games[gamename]['extpath']))
        ftpsend(ftp, zipped)
        os.remove(zipped)
        ftp.cwd('/')
        return
    else:
        ftp.mkd(gamename)
        backup(ftp, gamename)

def load(gamename, customsavename = None):
    if gamename in ftp.nlst():
        ftp.cwd(gamename)
        if customsavename:
            if customsavename in ftp.nlst():
                ftp.cwd(customsavename)
                files = ftp.nlst()
                for save in files:
                    ftpget(ftp, save, save)
            else:
                print("Error custom save does NOT exist... please resume from start after confirming name!")
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
                    else:
                        print("SCHMARRTY!!! FOLDER WAS EMPTY!!! LULL")
                        break
                        
                if choice == '2':
                    print("This option is under construction!")
                    break
                if choice == '3':
                    break
                else:
                    print("Invalid choice! please enter a number!")
    else:
        print("Saves of given game do NOT EXIST (DA FOQ) please resume from start after confirming name!")
    


welcome = ftpconn(config['FTP']['host'], typeensure(config['FTP']['port'], int), config['FTP']['user'], config['FTP']['password'])
print(welcome)
#backup(ftp, 'MINECRAFT')
load('MINECRAFT')
#print(os.getcwd())
#zipdir(str(os.getcwd()+'\\'+'temp'+'\\'+'MCBKUP'+str(time.time())), pathparser(games['MINECRAFT']['extpath']))
#str(os.getcwd()+'\\'+)
