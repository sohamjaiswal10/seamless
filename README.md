# seamless
A service which will be able to provide a cloud save like functionality to games which don't support it via ftp.

## usage
the script is supposed to connect to your own ftp server with a user in it which can save files the user would need complete permissions of the home directory, filezilla makes this easy to achieve so I recommend filezilla server for windows but the official server package has given me problems earlier so use the one provided with XAMPP. Change config.ini according to your server location, username and password to be able to connect

## ==MOST IMPORTANT==
PLEASE SET YOUR SYSTEM TIME CORRECTLY SEAMLESS USES EPOCH TIME TO NAME FILES IN THE FTP & currently seamless' limited game defaults only support win 10, that does not mean you can't get it to work on other stuff, you can easily if you poke around enough! I would encourage you to do so as it's so simple tbh. 

## ==ALSO IMPORTANT==
DO NOT MESS WITH THE FILESTRUCTURE IT MAKES IN THE USER HOME DIRECTORY PLZ

## ftp
Change config.ini accordingly for your own ftp server

## games
if you have changed the save directories of the games u need to change them in games.ini too

### 1


# Contribution
Contribute all you want, join the discord if you ever require help => 
[SUSHI: sohamjaiswal10's Discord](https://discord.gg/duPkZvF)