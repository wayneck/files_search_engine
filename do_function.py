# -*- coding: utf-8 -*-

import os
import time
from os import stat
import pymongo
import re
import codecs

FTP_PATH = "localhost:"# "ftp://10.10.10.1"
SEARCHPATH = "/home/wayne/win-d/workplace/python" #local abs file path

def displaySize(in_statinfo):
    file_size = in_statinfo.st_size
    if file_size > 1024000000:
        f_s = str("%.3f"%(file_size/1024/1024/1024) )+" GB"
        return f_s
    if file_size > 1024000:
        f_s = str("%.3f"%(file_size/1024/1024) )+" MB"
        return f_s
    if file_size > 1024:
        f_s = str("%.3f"%(file_size/1024) )+" KB"
        return f_s
    else:
        f_s = str("%.3f"%(file_size) )+" Byte"
        return f_s
def bad_filename(filename):
    return repr(filename)[1:-1]

def createFileDb(dbCol, file_dir):
    for root, dirs, files in os.walk(file_dir):
        if len(files) > 0:
            for file in files:
                per_record = []               
                if (type(root) != str):
                    root =root.decode('gb18030')
                    print(type(root))
                if (type(file) != str):
                    file = file.decode('gb18030')
                    print(type(file))           

                b2 = bytes('/', 'gb18030')
                file_fname_u8= root+'/'+file
                print(type(file_fname_u8))
                #file_fname= file_fname.encode("utf8","ignore")
                #file_fname = file_fname.encode('gb18030')
                #print(file_fname)
                #try:
                #    print(file)
                #except UnicodeEncodeError:
                #    print(bad_filename(file))
                per_record.append(file) #per_record[0]
                try:
                    statinfo =stat(file_fname_u8)
                except IOError:
                    print(file_fname_u8.encode('gb18030'))
                    
                    per_record.append("--") #per_record[1]
                    per_record.append("2021-01-24 09:59:42") #per_record[2]
                    per_record.append(root) #per_record[3]
                    per_record.append("--") #per_record[4]
                    per_record.append("--") #per_record[5]
                else:
                    print(file_fname_u8.encode('gb18030'))
                    per_record.append(displaySize(statinfo))
                    per_record.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(statinfo.st_atime)))
                    per_record.append(file_fname_u8)
                    per_record.append(statinfo.st_atime)
                    per_record.append(statinfo.st_size)
                if len(per_record)>=5:
                        add_record = {'f_name': per_record[0], 'f_length': per_record[1], 'f_time': per_record[2], 'f_path': per_record[3], 'sys_time': per_record[4], 'sys_size': per_record[5]}
                        dbCol.insert_one(add_record)

def deal_record(r_u):
    f_path = str(r_u['f_path']).replace(SEARCHPATH, FTP_PATH)
    return (str(r_u['f_name'])+','+str(r_u['f_time'])+','+str(r_u['f_length'])+','+f_path)
def searchByName(dbCol, s_text,sub_str):
    result_list=[]
    for u in dbCol.find({'f_name':re.compile(s_text)}):
        if len(sub_str) >0:
            first_str = str(u['f_name'])
            if (first_str.find(sub_str))>=0:
                print(u)
                result_list.append(deal_record(u))
        else:
            result_list.append(deal_record(u))
        
        print(u)

    return result_list

def searchByTime(dbCol, num):
    result_list=[]
    files = dbCol.find().sort("sys_time", -1)
    if(num <1 ):
        num = 20
    cnt=0
    for x in files:
      result_list.append(str(x['f_name']))
      cnt = cnt+1
      if(cnt>=20):
          break

    return result_list

def searchBySize(dbCol, s_text):
    result_list=[]
    for u in dbCol.find({'sys_size':re.compile(s_text)}):
        result_list.append(u)
        print(u)
    return result_list
    