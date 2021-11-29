# -*- coding: utf-8 -*-
 
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import time
import logging
import pymongo
import do_function
from datetime import timedelta

update_time = ""
#connect data base
myclient = pymongo.MongoClient("mongodb://localhost:27017/")


mydb = myclient['wayneDB']
mydb.profiling_info
collist = mydb.list_collection_names()
if "searchFileCache1" in collist:   # 判断 sites 集合是否存在
    searchDbCol = mydb["searchFileCache1"]
    print("集合已存在！")
else:
    searchDbCol = mydb["searchFileCache1"]
    do_function.createFileDb(searchDbCol, do_function.SEARCHPATH)
    update_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print("创建数据库完成！")


app = Flask(__name__)
# 设置静态文件缓存过期f_time
app.send_file_max_age_default = timedelta(seconds=1)

new_files = do_function.searchByTime(searchDbCol,-1)
 
@app.route('/search', methods=['POST', 'GET'])  # 添加路由

def search():
    #the newest file 20
    #if( len(new_files)<1):
    #    new_files = {'no file'}

    if request.method == 'POST':
        s_file_name = request.form.get("fileName")
        s_file_size = request.form.get("fileSize")
        s_file_time = request.form.get("fileTime")
        #user_input = "检索词语： "+s_file_name + "  检索文件大小： "+ s_file_size+ "  检索文件f_time： "+ s_file_time
        
        #basepath = os.path.dirname(__file__)  # 当前文件所在f_path
        exp_keyword = str(s_file_name).split('+')
        if(len(exp_keyword)>1):
            result_info = do_function.searchByName(searchDbCol, exp_keyword[0], exp_keyword[1])
        else:
            result_info = do_function.searchByName(searchDbCol, s_file_name, '')
        print( len(result_info) )
        user_input = "检索词： "+s_file_name + "  ： "+ str(len(result_info))+ "  个文件"

        return render_template('search_result.html',userinput=user_input , resultInfo =result_info, update_time=update_time)
        #flask_out2user.clear()
    print("search side")
    return render_template('search.html',new_files=new_files, update_time=update_time)

@app.route('/updateTable', methods=['POST', 'GET'])  # 添加路由
def table():
    if request.method == 'GET':
        print("begin refresh")
        try:
            mydb.collection.drop()
        except IOError:
            print("there is no cellect")
        searchDbCol = mydb["searchFileCache1"]
        do_function.createFileDb(searchDbCol, do_function.SEARCHPATH)
        print("refresh db over")
        update_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        updat_status= "搜索引擎"+update_time+"功能新完成"
    return render_template('updateTable.html',updat_status = updat_status)
if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=5000, debug=True)