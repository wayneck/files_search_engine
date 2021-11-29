
#   About This   
For local or remote filesystem search by mongoDB
use A or "+"  A+B  do search 


#   WORK PATH
FTP_PATH = "localhost:"# "ftp://10.10.10.1"     
SEARCHPATH = "/home/XXX/workplace" #local abs file path

#   Start Up

## pip package
pip3 -r requirements.txt
##  start
python3 search.py   
use web http://local:5000/search    
For first time execute, it build database will need take some time   
After that can use http://local:5000/updateTable update database    

