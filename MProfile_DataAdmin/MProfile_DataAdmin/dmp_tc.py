import pandas as pd
import numpy as np
import json
from sqlalchemy import create_engine
import urllib
from sqlalchemy import text
import xlrd
import os
from bs4 import BeautifulSoup
from sqlalchemy.types import NVARCHAR, Float, Integer

def mapping_df_types(df):
    dtypedict = {}
    for i, j in zip(df.columns, df.dtypes):
        if "object" in str(j):
            dtypedict.update({i: NVARCHAR(None)})
        if "float" in str(j):
            dtypedict.update({i: Float()})
        if "int" in str(j):
            dtypedict.update({i: Integer()})  
    return dtypedict


def fill_rpt(arr_l1,arr_l2,arr_l3,arr_l4,arr_l5,v_l1,v_l2,v_l3,v_l4,v_l5 ):
    arr_l1.append(v_l1)
    arr_l2.append(v_l2)
    arr_l3.append(v_l3)
    arr_l4.append(v_l4)
    arr_l5.append(v_l5)
    return


def static_crawl(path,arr_l1,arr_l2,arr_l3,arr_l4,arr_l5 ):
    dict_node = { '1':'人群概览|上传人数|uploadPopulationNum'
                 ,'2':'人群概览|覆盖人数|portrait-stat-item-num-large populationNum'
                 ,'3':'人群概览|匹配活跃用户数|activePopulationNum'
                 ,'4':'人群概览|性别|genTable'
                 ,'5':'人群概览|年龄|ageTable'
                 ,'6':'人群概览|学历|eduTable'
                 ,'7':'人群概览|地域|areaTable'
                 ,'8':'商业兴趣|广告点击偏好|businessInsTable_1018'
                 ,'9':'商业兴趣|代理类|Table_14734'
                 ,'10':'商业兴趣|房产家居类|Table_14725'
                 ,'11':'商业兴趣|服饰类|Table_14726'
                 ,'12':'商业兴趣|个人用品类|Table_14727'
                 ,'13':'商业兴趣|公共类|Table_14735'
                 ,'14':'商业兴趣|教育类|Table_14728'
                 ,'15':'商业兴趣|交通类|businessInsTable_14719'
                 ,'16':'商业兴趣|金融类|Table_14720'
                 ,'17':'商业兴趣|零售类|Table_14718'
                 ,'18':'商业兴趣|旅游类|Table_14729'
                 ,'19':'商业兴趣|其他类|Table_14733'
                 ,'20':'商业兴趣|日化类|Table_14722'
                 ,'21':'商业兴趣|食品饮料类|Table_14721'
                 ,'22':'商业兴趣|网络服务类|Table_14716'
                 ,'23':'商业兴趣|医疗服务类|Table_14731'
                 ,'24':'商业兴趣|娱乐消闲类|Table_14732'
                 ,'25':'商业兴趣|运营商类|Table_14724'
                 ,'26':'商业兴趣|游戏类|businessInsTable_14730'
                 ,'27':'商业兴趣|综合电商类|Table_14717'
                 ,'28':'商业兴趣|餐饮美食|Table_2436'
                 ,'29':'商业兴趣|房产|Table_2365'
                 ,'30':'商业兴趣|商业兴趣|businessInsTable_2317'
                 ,'31':'商业兴趣|服饰鞋帽箱包|businessInsTable_2391'
                 ,'32':'商业兴趣|互联网/电子产品|Table_2318'
                 ,'33':'商业兴趣|家居|Table_2358'
                 ,'34':'商业兴趣|金融|Table_2430'
                 ,'35':'商业兴趣|教育|businessInsTable_2373'
                 ,'36':'商业兴趣|旅游|businessInsTable_2383'
                 ,'37':'商业兴趣|美容|Table_2425'
                 ,'38':'商业兴趣|其他|Table_2332'
                 ,'39':'商业兴趣|生活服务|Table_2419'
                 ,'40':'商业兴趣|体育运动|Table_2325'
                 ,'41':'商业兴趣|汽车|businessInsTable_2402'
                 ,'42':'商业兴趣|商务服务|businessInsTable_2340'
                 ,'43':'商业兴趣|医疗健康|Table_2334'
                 ,'44':'商业兴趣|孕产育儿|Table_2354'
                 ,'45':'商业兴趣|政法|Table_2371'
                 ,'46':'商业兴趣|游戏|businessInsTable_2410'
                 ,'47':'工具应用|APP活跃倾向|toolAppTable_9664'
                 ,'48':'工具应用|办公商务|Table_9865'
                 ,'49':'工具应用|餐饮|Table_9888'
                 ,'50':'工具应用|电话通讯|Table_9914'
                 ,'51':'工具应用|房产|Table_9793'
                 ,'52':'工具应用|家政/社区|Table_9837'
                 ,'53':'工具应用|健康美容|Table_9817'
                 ,'54':'工具应用|教育培训|toolAppTable_9849'
                 ,'55':'工具应用|金融理财|toolAppTable_9776'
                 ,'56':'工具应用|快递|Table_9894'
                 ,'57':'工具应用|旅游出行|toolAppTable_9806'
                 ,'58':'工具应用|汽车服务|toolAppTable_9755'
                 ,'59':'工具应用|汽车品牌|toolAppTable_17398'
                 ,'60':'工具应用|人力资源|toolAppTable_9897'
                 ,'61':'工具应用|生活服务|toolAppTable_9822'
                 ,'62':'工具应用|实用工具|toolAppTable_9920'
                 ,'63':'工具应用|数字阅读|Table_9930'
                 ,'64':'工具应用|图像服务|Table_9905'
                 ,'65':'工具应用|医疗服务|Table_9910'
                 ,'66':'工具应用|系统工具|toolAppTable_9936'
                 ,'67':'工具应用|新闻资讯|toolAppTable_9857'
                 ,'68':'工具应用|移动购物|toolAppTable_9840'
                 ,'69':'工具应用|移动社交|Table_9800'
                 ,'70':'工具应用|移动音乐|Table_9871'
                 ,'71':'工具应用|育儿母婴|Table_9769'
                 ,'72':'工具应用|移动视频|toolAppTable_9878'
                 ,'73':'工具应用|游戏|toolAppTable_9665'
                 ,'74':'工具应用|智能设备|Table_9948'
                 ,'75':'工具应用|主题美化|Table_9953'
                 ,'76':'媒体兴趣爱好|汽车兴趣|mediaInsTable_3918'
                 ,'77':'媒体兴趣爱好|车型|Table_3919'
                 ,'78':'媒体兴趣爱好|国别|mediaInsTable_3923'
                 ,'79':'媒体兴趣爱好|级别|mediaInsTable_3955'
                 ,'80':'媒体兴趣爱好|价位|mediaInsTable_3945'
                 ,'81':'媒体兴趣爱好|排量|mediaInsTable_3937'
                 ,'82':'媒体兴趣爱好|用途|mediaInsTable_3974'
                 ,'83':'娱乐兴趣|视频浏览偏好|entertainmentInsTable_11'
                 ,'84':'娱乐兴趣|观看平台|Table_4810'
                 ,'85':'娱乐兴趣|视频时长|Table_385'
                 ,'86':'娱乐兴趣|网络接入|Table_4812'
                 ,'87':'娱乐兴趣|观看时间|entertainmentInsTable_4809'
                 ,'88':'娱乐兴趣|剧集类型|entertainmentInsTable_70'
                 ,'89':'娱乐兴趣|视频频道|entertainmentInsTable_12'
                 ,'90':'娱乐兴趣|演员|entertainmentInsTable_135'
                 ,'91':'娱乐兴趣|制片地区|entertainmentInsTable_114'
                 }

    soup = BeautifulSoup(open(path,'r',encoding='UTF-8'))
    for key in dict_node.keys():
        try :
            if   key in ['2']: #no table & only class name
                if soup.find("span",class_ = dict_node[key].split('|')[2])  is not None:  
                    tmp = soup.find("span",class_ = dict_node[key].split('|')[2]).get_text()
                    fill_rpt(arr_l1,arr_l2,arr_l3,arr_l4,arr_l5,dict_node[key].split('|')[0],dict_node[key].split('|')[1],dict_node[key].split('|')[1],'N/A',tmp )           
            elif key in ['1','3']: #no table & id
                if soup.find(id = dict_node[key].split('|')[2])  is not None: 
                    tmp = soup.find(id = dict_node[key].split('|')[2]).get_text()
                    fill_rpt(arr_l1,arr_l2,arr_l3,arr_l4,arr_l5,dict_node[key].split('|')[0],dict_node[key].split('|')[1],dict_node[key].split('|')[1],'N/A',tmp )           
            elif key in [ '4','5','6','9','10','11','12','13','14','16','17','18','19','20','21','22','23','24','25','27','28','29','32','33','34','37','38','39','40','43','44','45','48','49','50','51','52','53','56','63','64','65','69','70','71','74','75','77','84','85','86']: #table & no rank
                if soup.find(id=dict_node[key].split('|')[2]) is not None: 
                    tmplist = soup.find(id=dict_node[key].split('|')[2]).find('table').find('tbody').find_all('tr')
                    for item in tmplist:
                        dmitem     = item.find_all('td')[0].find('div',class_='mini-table-td-content').get_text().strip()
                        percentage = item.find_all('td')[1].find('div',class_='mini-table-td-div u-paddingH30').get_text().strip()
                        tgi        = item.find_all('td')[2].find('div',class_='mini-table-td-div u-paddingH30').get_text().strip()
                        fill_rpt(arr_l1,arr_l2,arr_l3,arr_l4,arr_l5,dict_node[key].split('|')[0],dict_node[key].split('|')[1],'占比',dmitem,percentage )
                        fill_rpt(arr_l1,arr_l2,arr_l3,arr_l4,arr_l5,dict_node[key].split('|')[0],dict_node[key].split('|')[1],'TGI',dmitem,tgi )
            else : #table & rank
                if soup.find(id=dict_node[key].split('|')[2]) is not None:     
                    tmplist = soup.find(id=dict_node[key].split('|')[2]).find('table').find('tbody').find_all('tr')
                    for item in tmplist:
                        if item.find_all('td')[0].find('div',class_='mini-table-td-div ') is not None:
                           dmitem     = item.find_all('td')[1].find('div',class_='mini-table-td-div ').get_text().strip()
                           percentage = item.find_all('td')[2].find('div',class_='mini-table-td-div ').get_text().strip()
                           tgi        = item.find_all('td')[3].find('div',class_='mini-table-td-div u-width90').get_text().strip()
                           rank       = item.find_all('td')[0].find('div',class_='mini-table-td-div ').get_text().strip()
                           fill_rpt(arr_l1,arr_l2,arr_l3,arr_l4,arr_l5,dict_node[key].split('|')[0],dict_node[key].split('|')[1],'排名',dmitem,rank )
                           fill_rpt(arr_l1,arr_l2,arr_l3,arr_l4,arr_l5,dict_node[key].split('|')[0],dict_node[key].split('|')[1],'占比',dmitem,percentage )
                           fill_rpt(arr_l1,arr_l2,arr_l3,arr_l4,arr_l5,dict_node[key].split('|')[0],dict_node[key].split('|')[1],'TGI',dmitem,tgi )
        except:
            print(key)
    return

def dmp_tc(i_sid,i_udpath):  
    ##DB Config    
    #params = urllib.parse.quote_plus('DRIVER={ODBC Driver 13 for SQL Server};SERVER=(local) ;DATABASE=Test;DSN=(local);Trusted_Connection=yes')
    params = urllib.parse.quote_plus('DRIVER={ODBC Driver 13 for SQL Server};SERVER=52.80.196.236 ;DATABASE=mprofile_dev;UID=mprofile;PWD=mprofile_2018')
    conn = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)    
    #conn = create_engine("mssql+pymssql://mprofile:mprofile_2018@52.80.196.236/mprofile_dev") 
    segment_id = i_sid
    tc_folder  = i_udpath
    
    #版面
    arr_l1 = []
    #图表区域
    arr_l2 = []
    #度量
    arr_l3 = []
    #维度元素
    arr_l4 = []
    #数值
    arr_l5 = []
    inpath  = tc_folder
    list = os.listdir(inpath)
    try:
        for i in range(0,len(list)):
            path = os.path.join(inpath,list[i])
            if os.path.isfile(path):
                   static_crawl(path,arr_l1,arr_l2,arr_l3,arr_l4,arr_l5 ) 
        arr_l0 = np.repeat(segment_id,len(arr_l1))
        dict_report = {'SEGMENT_ID':arr_l0,'SECTION':arr_l1,'TAG_NAME':arr_l2,'KPI':arr_l3,'OPTION':arr_l4,'VALUE':arr_l5}
        report = pd.DataFrame(dict_report)
        report = report.drop_duplicates()    
        #report.to_csv('C://App//Admin//Archive3//report_test.csv' ,index=False,header= True)
        stid  = 0 
        endid = 0
    
        for i in range(int( np.ceil(len(report)/300)) ):
            stid  = i*300
            endid = (i+1)*300
            tdf  = report[stid:endid]
            if stid == 0:
               tdf.to_sql('Tencent_Temp', con=conn,if_exists='replace' ,index=False,dtype=mapping_df_types(tdf))
            else:
               tdf.to_sql('Tencent_Temp', con=conn,if_exists='append' ,index=False,dtype=mapping_df_types(tdf))
    finally:
         for file02_item in os.listdir(tc_folder):
             os.remove(tc_folder+'/'+file02_item);