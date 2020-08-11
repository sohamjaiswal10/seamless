import time

def namer(gamename):
    name = gamename + str(time.time())[0:10]
    return name

def rev(string):
    return(string[::-1])

def typeensure(var,typ):
    try:
        var = typ(var)
    except ValueError:
        print("Sorry the type cannot be converted to what it's supposed to be... try again")
        var = input(f"Enter the thing which will be convertible to %s type" %str(typ))
        typeensure(var, typ)
    finally:
        return(var)