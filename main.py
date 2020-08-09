#PLEASE DO NOT MESS AROUND IF U DON'T KNOW WHAT YOU ARE DOING
#YOU WILL BE HANDLING FILES OUTSIDE THE CWD, DATA ON THE 
#MAY BE LOST IF YOU DO NOT KNOW WHAT YOU ARE DOING!

#importing libraries which may be required...
import os
import zipfile, shutil
from ftplib import FTP
from configparser import ConfigParser

#made an ftp object to connect to
ftp = FTP() 
config = ConfigParser()
config.read('games.ini')

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
#filename (str) is of the file which is to be got
#local (open file object) is where it's data is saved.
def ftpget(ftp, filename, local):
    file = open(local, 'wb')
    ftp.retrbinary('RETR ' + filename, file.write, 1024)
    file.close()

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
    if ftp.voidcmd("NOOP"):
        ftp.close()
    

        
