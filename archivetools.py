import zipfile, shutil

#direct is the directory, out is the file
def zipdir(out, direct): 
    shutil.make_archive(out, 'zip', direct)
    return

#to unzip saves, path is where the zip is, direct is where to save zip
def extract(path, direct): 
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(direct)
    return