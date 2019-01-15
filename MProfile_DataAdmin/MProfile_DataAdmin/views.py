# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,Flask,jsonify,abort,request,send_from_directory,url_for
from MProfile_DataAdmin import app
import time
from sqlalchemy import create_engine,text
import urllib
import json
from   werkzeug import secure_filename
import pandas as pd
import numpy  as np
import os
import sys
import xlrd
from   concurrent.futures import ThreadPoolExecutor
from   MProfile_DataAdmin.bckend01 import bckend01



ALLOWED_EXTENSIONS = set(['txt', 'csv', 'png', 'jpg', 'jpeg', 'html','xls'])
app.config['UPLOAD_FOLDER']  = 'MProfile_DataAdmin/static/uploads/ud'
app.config['UPLOAD_FOLDER2'] = 'MProfile_DataAdmin/static/uploads/tc'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )



@app.route('/ready', methods=['GET'])
def get_ready():
    params = urllib.parse.quote_plus('DRIVER={ODBC Driver 13 for SQL Server};SERVER=52.80.196.236 ;DATABASE=mprofile_dev;UID=mprofile;PWD=mprofile_2018')
    conn = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)     
    conn_2 = conn.connect()    
    result2 = conn_2.execute("select segmentid,segmentname,advertiser,size,createtime,status,minsights,tdmp,up,td,ud,action from uv_Segment_List_Admin order by createtime desc")
    a=result2.fetchall()
    conn_2.close()
    jsonstr = []
    for i in range(len(a)):
        jsonstr.append( {"segmentid":a[i][0],"segmentname":a[i][1],"advertiser":a[i][2],"size":a[i][3],"createtime":a[i][4],"status":a[i][5],"minsights":a[i][6],"tdmp":a[i][7],"up":a[i][8],"td":a[i][9],"ud":a[i][10],"action":a[i][11]})
    return jsonify(jsonstr)

@app.route('/filter01', methods=['GET'])
def get_filter():
    sid    = str(request.args.get('sid'));
    adv    = str(request.args.get('adv'));
    idate  = str(request.args.get('idate'));
    stts   = str(request.args.get('stts'));

    params = urllib.parse.quote_plus('DRIVER={ODBC Driver 13 for SQL Server};SERVER=52.80.196.236 ;DATABASE=mprofile_dev;UID=mprofile;PWD=mprofile_2018')
    conn = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)      
    conn_2 = conn.connect()    

    qrytxt = "select segmentid,segmentname,advertiser,size,createtime,status,minsights,tdmp,up,td,ud,action from uv_Segment_List_Admin "

    if   len(sid) == 0 and len(adv) == 0 and len(idate) == 0 and len(stts) == 0 :
         result2 = conn_2.execute(qrytxt+" order by createtime desc")
    elif len(sid) == 0 and len(adv) == 0 and len(idate) == 0:
         qrytxt = qrytxt + "where status = :status order by createtime desc"
         result2 = conn_2.execute(text(qrytxt),status=stts)
    elif len(sid) == 0 and len(adv) == 0 and len(stts) == 0:
         qrytxt = qrytxt + "where createtime>=:idate and createtime< DATEADD(day,1,:idate) order by createtime desc"
         result2 = conn_2.execute(text(qrytxt),idate=idate)
    elif len(sid) == 0 and len(stts) == 0 and len(idate) == 0:
         qrytxt = qrytxt + "where advertiser =:advertiser order by createtime desc"
         result2 = conn_2.execute(text(qrytxt),advertiser=adv)
    elif len(idate) == 0 and len(stts) == 0 and len(adv) == 0:
         qrytxt = qrytxt + "where  (segmentid = :segmentid or segmentname =:segmentid) order by createtime desc"
         result2 = conn_2.execute(text(qrytxt),segmentid=sid)
    elif len(idate) == 0 and len(stts) == 0:
         qrytxt = qrytxt + "where  (segmentid = :segmentid or segmentname =:segmentid) and advertiser =:advertiser order by createtime desc"
         result2 = conn_2.execute(text(qrytxt),segmentid=sid,advertiser=adv)
    elif len(idate) == 0 and len(adv) == 0:
         qrytxt = qrytxt + "where  (segmentid = :segmentid or segmentname =:segmentid) and status = :status order by createtime desc"
         result2 = conn_2.execute(text(qrytxt),segmentid=sid,status=stts)
    elif len(idate) == 0 and len(sid) == 0:
         qrytxt = qrytxt + "where   advertiser =:advertiser and status = :status order by createtime desc"
         result2 = conn_2.execute(text(qrytxt),advertiser=adv,status=stts)
    elif len(sid) == 0 and len(adv) == 0:
         qrytxt = qrytxt + "where (createtime>=:idate and createtime< DATEADD(day,1,:idate)) and status = :status order by createtime desc"
         result2 = conn_2.execute(text(qrytxt),idate=idate,status=stts)
    elif len(stts) == 0 and len(adv) == 0:
         qrytxt = qrytxt + "where (createtime>=:idate and createtime< DATEADD(day,1,:idate)) and (segmentid = :segmentid or segmentname =:segmentid) order by createtime desc"
         result2 = conn_2.execute(text(qrytxt),idate=idate,segmentid=sid)
    elif len(sid) == 0 and len(stts) == 0:
         qrytxt = qrytxt + "where (createtime>=:idate and createtime< DATEADD(day,1,:idate)) and advertiser =:advertiser order by createtime desc"
         result2 = conn_2.execute(text(qrytxt),idate=idate,advertiser=adv)
    elif len(sid) == 0:
         qrytxt = qrytxt + "where (createtime>=:idate and createtime< DATEADD(day,1,:idate)) and advertiser =:advertiser and status = :status order by createtime desc"
         result2 = conn_2.execute(text(qrytxt),idate=idate,advertiser=adv,status=stts)
    elif len(idate) == 0:
         qrytxt = qrytxt + "where (segmentid = :segmentid or segmentname =:segmentid) and advertiser =:advertiser and status = :status order by createtime desc"
         result2 = conn_2.execute(text(qrytxt),segmentid=sid,advertiser=adv,status=stts)
    elif len(adv) == 0:
         qrytxt = qrytxt + "where (segmentid = :segmentid or segmentname =:segmentid) and (createtime>=:idate and createtime< DATEADD(day,1,:idate)) and status = :status order by createtime desc"
         result2 = conn_2.execute(text(qrytxt),segmentid=sid,idate=idate,status=stts)
    elif len(stts) == 0:
         qrytxt = qrytxt + "where (segmentid = :segmentid or segmentname =:segmentid) and (createtime>=:idate and createtime< DATEADD(day,1,:idate)) and advertiser = :advertiser order by createtime desc"
         result2 = conn_2.execute(text(qrytxt),segmentid=sid,idate=idate,advertiser=adv)
    else:
         qrytxt = qrytxt + "where (segmentid = :segmentid or segmentname =:segmentid) and (createtime>=:idate and createtime< DATEADD(day,1,:idate)) and advertiser = :advertiser and status = :status order by createtime desc"
         result2 = conn_2.execute(text(qrytxt),segmentid=sid,idate=idate,advertiser=adv,status=stts)
    a=result2.fetchall()
    conn_2.close()
    jsonstr = []
    for i in range(len(a)):
        jsonstr.append( {"segmentid":a[i][0],"segmentname":a[i][1],"advertiser":a[i][2],"size":a[i][3],"createtime":a[i][4],"status":a[i][5],"minsights":a[i][6],"tdmp":a[i][7],"up":a[i][8],"td":a[i][9],"ud":a[i][10],"action":a[i][11]})
    return jsonify(jsonstr)


@app.route('/up_00', methods=['POST'])
def post_fileup00():
    """Renders the about page."""
    jsonstr = []
    if request.method == 'POST':
        bid = int(request.args.get('bid', 0))
        idv = request.args.get('idv')
        if bid==2 :
            if  os.path.exists(app.config['UPLOAD_FOLDER2']+'/'+idv):                
                for i in os.listdir(app.config['UPLOAD_FOLDER2']+'/'+idv):
                    os.remove(app.config['UPLOAD_FOLDER2']+'/'+idv+'/'+i)                
                os.removedirs(app.config['UPLOAD_FOLDER2']+'/'+idv)
            os.mkdir(app.config['UPLOAD_FOLDER2']+'/'+idv)    
            file02 = request.files.getlist('file02')
            for file02_item in file02:
                if file02_item and allowed_file(file02_item.filename):
                    filename02 = secure_filename(file02_item.filename)   
                    path_url02 = app.config['UPLOAD_FOLDER2'] +'/'+idv+'/'+filename02
                    file02_item.save(path_url02)
        else:
            if  os.path.exists(app.config['UPLOAD_FOLDER']+'/'+idv):                
                for i in os.listdir(app.config['UPLOAD_FOLDER']+'/'+idv):
                    os.remove(app.config['UPLOAD_FOLDER']+'/'+idv+'/'+i)                
                os.removedirs(app.config['UPLOAD_FOLDER']+'/'+idv)
            os.mkdir(app.config['UPLOAD_FOLDER']+'/'+idv)
            file01 = request.files['file01']
            if file01 and allowed_file(file01.filename):
                filename = secure_filename(file01.filename)   
                path_url = app.config['UPLOAD_FOLDER'] +'/'+idv+'/'+filename
                file01.save(path_url)        
    jsonstr.append( {"status":1})
    return jsonify(jsonstr)

@app.route('/stsup01', methods=['PUT'])
def put_stsup01():
    idv = request.args.get('sid');
    #params = urllib.parse.quote_plus('DRIVER={ODBC Driver 13 for SQL Server};SERVER=(local) ;DATABASE=Test;DSN=(local);Trusted_Connection=yes')
    params = urllib.parse.quote_plus('DRIVER={ODBC Driver 13 for SQL Server};SERVER=52.80.196.236 ;DATABASE=mprofile_dev;UID=mprofile;PWD=mprofile_2018')
    conn = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)    
    #conn = create_engine("mssql+pymssql://mprofile:mprofile_2018@52.80.196.236/mprofile_dev") 
    conn_2 = conn.connect()
    conn_2.execute(text("UPDATE Segment_WD_Status SET Status = 2 WHERE DMP_ID in (2,5) and Segment_ID = :segmentid").execution_options(autocommit=True),segmentid=idv)
    conn_2.execute(text("UPDATE Segment SET Status_ID = 2 WHERE Segment_ID = :segmentid").execution_options(autocommit=True),segmentid=idv)
    conn_2.close()
    return jsonify({"status":1})


@app.route('/submit01', methods=['POST'])
def post_submit01():
    jsonstr = []
    l_path_url01 = []
    executor = ThreadPoolExecutor(2)
    
    if request.method == 'POST':
        sid = request.args.get('sid')
        try:
            for file01_item in os.listdir(app.config['UPLOAD_FOLDER']+'/'+sid):
                l_path_url01.append(app.config['UPLOAD_FOLDER']+'/'+ sid +'/'+file01_item);
            executor.submit(bckend01,sid,l_path_url01[0],app.config['UPLOAD_FOLDER2']+'/'+sid);
        except:
            params = urllib.parse.quote_plus('DRIVER={ODBC Driver 13 for SQL Server};SERVER=52.80.196.236 ;DATABASE=mprofile_dev;UID=mprofile;PWD=mprofile_2018')
            conn = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)   
            conn_2 = conn.connect()
            conn_2.execute(text("UPDATE Segment_WD_Status SET Status = -1 WHERE DMP_ID in (2,5) and Segment_ID = :segmentid").execution_options(autocommit=True),segmentid=idv)
            conn_2.close()
    jsonstr.append( {"status":1})
    return jsonify(jsonstr)
    
