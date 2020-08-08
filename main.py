#importing libraries which may be required...
import os
import zipfile, shutil
from ftplib import FTP

def zipdir(direct, out): #direct is the directory, out is the file
    shutil.make_archive(out, 'zip', direct)
#==usage==
#zipf = zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED)
#zipdir('tmp/', zipf)
#zipf.close()

def extract(path, direct): #to unzip saves, path is where the zip is, direct is where to save zip
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(direct)

def ftpconn(host,port,usr,pswd,dir='/'):#if u don't get this then u r unqualified to be here
    global ftp
    ftp = FTP()
    ftp.connect(host,port)
    ftp.login(user=usr, passwd=pswd)
    return(ftp.getwelcome())

def ftpget(ftp, filename, local):#filename (str) is of the file which is to be got, local (open file object) is where it's data is saved.
    file = open(local, 'wb')
    ftp.retrbinary('RETR ' + filename, file.write, 1024)
    file.close()

def ftpsend(ftp, filename):
    ftp.storbinary('STOR '+filename, open(filename, 'rb'))
    
    




