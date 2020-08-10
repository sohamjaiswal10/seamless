#PLEASE DO NOT MESS AROUND IF U DON'T KNOW WHAT YOU ARE DOING
#YOU WILL BE HANDLING FILES OUTSIDE THE CWD, DATA ON THE 
#MAY BE LOST IF YOU DO NOT KNOW WHAT YOU ARE DOING!

#importing libraries which may be required...
import os, sys
import zipfile, shutil
from ftplib import FTP
from configparser import ConfigParser

#made an ftp object to connect to
ftp = FTP()

#made an openlist list to keep track of open files, so that program closes safely
#without corrupting anything
openlist=[]

#made a games configparser object to read specific profiles for games from games.ini
games = ConfigParser()
games.read('games.ini')

#made a config configparser object to read configuration for ftp in config.ini
config = ConfigParser()
config.read('config.ini')

#direct is the directory, out is the file
def zipdir(direct, out): 
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

def typeensure(var,typ,num):
    if num == 0:
        try:
            typ = typ(var)
        except:
            print("Sorry the type cannot be converted to what it's supposed to be... try again")
            var = input(f"Enter the thing which will be convertible to %s type" %str(typ))
            typeensure(var, typ, num+1)
        finally:
            return(typ)
    else:
        if num != 0:
            try:
                typ = typ(var)
            except:
                print("Sorry the type cannot be converted to what it's supposed to be... try again")
                var = input(f"Enter the thing which will be convertible to %s type" %str(typ))
                typeensure(var, typ, num+1)
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

def backupall():
    pass

    

        
