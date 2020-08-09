#importing libraries which may be required...
import os
import zipfile, shutil
from ftplib import FTP

ftp = FTP() #made an ftp object to connect to

def zipdir(direct, out): #direct is the directory, out is the file
    shutil.make_archive(out, 'zip', direct)
#==usage==
#zipf = zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED)
#zipdir('tmp/', zipf)
#zipf.close()

def extract(path, direct): #to unzip saves, path is where the zip is, direct is where to save zip
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(direct)

def ftpconn(host,port=21, usr='anonymous', pswd='',dir='/'):#if u don't get this then u r unqualified to be here
    ftp.connect(host,port)
    ftp.login(user=usr, passwd=pswd)
    return(ftp.getwelcome())

def ftpget(ftp, filename, local):#filename (str) is of the file which is to be got, local (open file object) is where it's data is saved.
    file = open(local, 'wb')
    ftp.retrbinary('RETR ' + filename, file.write, 1024)
    file.close()

def ftpsend(ftp, filename):
    ftp.storbinary('STOR '+filename, open(filename, 'rb'))

def typeensure(var,typ,num):
    if num == 0:
        try:
            typ = typ(var)
        else:
            print("Sorry the type cannot be converted to what it's supposed to be... try again")
            var = input(f"Enter the thing which will be convertible to %s type" %str(typ))
            typeensure(var, typ, num+1)
        finally:
            return(typ)
    else:
        if num != 0:
            try:
                typ = typ(var)
            else:
                print("Sorry the type cannot be converted to what it's supposed to be... try again")
                var = input(f"Enter the thing which will be convertible to %s type" %str(typ))
                typeensure(var, typ, num+1)
            finally:
                return(typ)
        


def fin():
    if ftp.voidcmd("NOOP"):
        ftp.close()
    
def interface():
    while True:
        if ftp.voidcmd("NOOP") == False:
            choice = input('''
What would you like to do?
1) Connect to an ftp with username and password
2) Connect to ftp anonymously
3) Close ftp connection

''')
            if choice == '1':
                host = input("Enter hostname: ")
                port = input("Enter port: ")
                typeensure(port, int, 0)
                user = input("Enter username: ")
                password = input("Enter password of user: ")
                subdir = input("Enter subdir loc(If available/need be): ")
                ftpconn(host,port,user,password,subdir)
            elif choice == '2':
                pass
            elif choice == '3':
                fin()
        

