import pandas as pd
import numpy as np
import json
from sqlalchemy import create_engine
import urllib
from sqlalchemy import text
import xlrd
import os
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


def dmp_ud(i_sid,i_udpath):
    #params = urllib.parse.quote_plus('DRIVER={ODBC Driver 13 for SQL Server};SERVER=(local) ;DATABASE=Test;DSN=(local);Trusted_Connection=yes')
    params = urllib.parse.quote_plus('DRIVER={ODBC Driver 13 for SQL Server};SERVER=52.80.196.236 ;DATABASE=mprofile_dev;UID=mprofile;PWD=mprofile_2018')
    conn = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)    
    #conn = create_engine("mssql+pymssql://mprofile:mprofile_2018@52.80.196.236/mprofile_dev") 

    segment_id = i_sid
    ud_path    = i_udpath
    xls_file = pd.ExcelFile(ud_path)
    try:
        table2 = xls_file.parse('基础属性',header=None)
        table3 = xls_file.parse('地域属性',header=None)
        table4 = xls_file.parse('消费属性',header=None)
        table5 = xls_file.parse('兴趣偏好',header=None)
        ################################################################# table 2 ##########################################################

        secid      =0
        tblid      =0
        colid      =0
        p_colid    =0
        cttid      =0
        p_cttid    =0
        p_ind      =0
        table_name2 = ""
        col_name2_1   =list('')
        col_name2_2   =list('')
        col_name2_3   =list('')
        col_name2_4   =list('')
        col_name2_5   =list('')
        arr2_1 = []
        arr2_2 = []
        arr2_3 = []
        arr2_4 = []
        arr2_5 = []


        for index, row in table2.iterrows():
            cnt_nn = 0
            for i in range(len(tuple(row))):
                if  pd.isnull(tuple(row)[i]):
                    cnt_nn+= 1      
            ind =  len(tuple(row)) - cnt_nn
    
            if  ind !=0 :
                if ind == 1:
                    tblid =1
                else:
                    tblid =0
                    if  p_ind   ==  1 :
                        colid = 1
                    else:
                        colid = 0            
                    if  (p_colid == 1) or (p_cttid ==1):
                        cttid = 1
                    else:
                        cttid = 0          
                secid = 1
            else:        
                secid = 0
                tblid = 0
                colid = 0
                cttid = 0
            if   secid ==1 and tblid== 1:
                 rflag = 't'
            elif secid ==1 and colid== 1:
                 rflag = 'c'
            elif secid ==1 and cttid== 1:
                 rflag = 'r'
            else:
                 rflag = 'n'
  
            if   rflag == 't':
                 table_name2 = row[0]
            elif rflag == 'c':
                if   table_name2 in ('性别'):
                     col_name2_1   = [ 'OPTION' if x in ('选项') else 'PCT' if x in ('百分比') else x  for x in list(row)] 
                elif table_name2 in ('年龄'):
                     col_name2_2   = [ 'OPTION' if x in ('选项') else 'PCT' if x in ('百分比') else x  for x in list(row)]
                elif table_name2 in ('职业'):
                     col_name2_3   = [ 'OPTION' if x in ('选项') else 'PCT' if x in ('百分比') else x  for x in list(row)]
                elif table_name2 in ('学历'):
                     col_name2_4   = [ 'OPTION' if x in ('选项') else 'PCT' if x in ('百分比') else x  for x in list(row)]
                elif table_name2 in ('人生阶段'):
                     col_name2_5   = [ 'OPTION' if x in ('选项') else 'PCT' if x in ('百分比') else x  for x in list(row)]   
            elif rflag == 'r':
                 if   table_name2 in ('性别'):
                      arr2_1.append(tuple(row))
                 elif table_name2 in ('年龄'):
                      arr2_2.append(tuple(row))
                 elif table_name2 in ('职业'):
                      arr2_3.append(tuple(row))
                 elif table_name2 in ('学历'):
                      arr2_4.append(tuple(row))
                 elif table_name2 in ('人生阶段'):
                      arr2_5.append(tuple(row))
     
            p_ind   =  ind
            p_colid =  colid
            p_cttid =  cttid         
    
        pdf2_1 = pd.DataFrame(arr2_1 ,index = None,columns = col_name2_1) 
        pdf2_2 = pd.DataFrame(arr2_2 ,index = None,columns = col_name2_2)
        pdf2_3 = pd.DataFrame(arr2_3 ,index = None,columns = col_name2_3)
        pdf2_4 = pd.DataFrame(arr2_4 ,index = None,columns = col_name2_4)
        pdf2_5 = pd.DataFrame(arr2_5 ,index = None,columns = col_name2_5)

        df2_1  = pd.concat([pd.DataFrame( np.repeat(segment_id,len(pdf2_1)),index = None,columns = ['SEGMENT_ID'] ),pdf2_1],axis =1 )  
        df2_2  = pd.concat([pd.DataFrame( np.repeat(segment_id,len(pdf2_2)),index = None,columns = ['SEGMENT_ID'] ),pdf2_2],axis =1 )       
        df2_3  = pd.concat([pd.DataFrame( np.repeat(segment_id,len(pdf2_3)),index = None,columns = ['SEGMENT_ID'] ),pdf2_3],axis =1 )      
        df2_4  = pd.concat([pd.DataFrame( np.repeat(segment_id,len(pdf2_4)),index = None,columns = ['SEGMENT_ID'] ),pdf2_4],axis =1 )  
        df2_5  = pd.concat([pd.DataFrame( np.repeat(segment_id,len(pdf2_5)),index = None,columns = ['SEGMENT_ID'] ),pdf2_5],axis =1 )  

        fdf2_1  = pd.concat([pd.DataFrame( np.repeat(201,len(df2_1)),index = None,columns = ['TAG_CD'] ),df2_1],axis =1 )  
        fdf2_2  = pd.concat([pd.DataFrame( np.repeat(202,len(df2_2)),index = None,columns = ['TAG_CD'] ),df2_2],axis =1 )       
        fdf2_3  = pd.concat([pd.DataFrame( np.repeat(203,len(df2_3)),index = None,columns = ['TAG_CD'] ),df2_3],axis =1 )      
        fdf2_4  = pd.concat([pd.DataFrame( np.repeat(204,len(df2_4)),index = None,columns = ['TAG_CD'] ),df2_4],axis =1 )  
        fdf2_5  = pd.concat([pd.DataFrame( np.repeat(205,len(df2_5)),index = None,columns = ['TAG_CD'] ),df2_5],axis =1 ) 





        fdf2_1.to_sql('AliUnidesk_Temp', con=conn,if_exists='replace',index=False,dtype=mapping_df_types(fdf2_1))
        fdf2_2.to_sql('AliUnidesk_Temp', con=conn,if_exists='append' ,index=False,dtype=mapping_df_types(fdf2_2))
        fdf2_3.to_sql('AliUnidesk_Temp', con=conn,if_exists='append' ,index=False,dtype=mapping_df_types(fdf2_3))
        fdf2_4.to_sql('AliUnidesk_Temp', con=conn,if_exists='append' ,index=False,dtype=mapping_df_types(fdf2_4))
        fdf2_5.to_sql('AliUnidesk_Temp', con=conn,if_exists='append' ,index=False,dtype=mapping_df_types(fdf2_5))

        ##################################################################################table4#####################################
        secid      =0
        tblid      =0
        colid      =0
        p_colid    =0
        cttid      =0
        p_cttid    =0
        p_ind      =0

        table_name4 = ""

        col_name4_1   =list('')
        col_name4_2   =list('')
        col_name4_3   =list('')
        col_name4_4   =list('')

        arr4_1 = []
        arr4_2 = []
        arr4_3 = []
        arr4_4 = []


        for index, row in table4.iterrows():
            cnt_nn = 0
            for i in range(len(tuple(row))):
                if  pd.isnull(tuple(row)[i]):
                    cnt_nn+= 1    
            ind =  len(tuple(row)) - cnt_nn
            if  ind !=0 :
                if ind == 1:
                    tblid =1
                else:
                    tblid =0
                    if  p_ind   ==  1 :
                        colid = 1
                    else:
                        colid = 0            
                    if  (p_colid == 1) or (p_cttid ==1):
                        cttid = 1
                    else:
                        cttid = 0          
                secid = 1
            else:        
                secid = 0
                tblid = 0
                colid = 0
                cttid = 0
        
            if   secid ==1 and tblid== 1:
                 rflag = 't'
            elif secid ==1 and colid== 1:
                 rflag = 'c'
            elif secid ==1 and cttid== 1:
                 rflag = 'r'
            else:
                 rflag = 'n'

            if   rflag == 't':
                 table_name4 = row[0]
            elif rflag == 'c':
                if   table_name4 in ('月均消费金额'):
                     col_name4_1   = [ 'OPTION' if x in ('选项') else 'PCT' if x in ('百分比') else x  for x in list(row) if not pd.isnull(x) ]
                elif table_name4 in ('一级类目偏好'):
                     col_name4_2   = [ 'OPTION' if x in ('选项') else 'PCT' if x in ('百分比') else x  for x in list(row) if not pd.isnull(x)  ]
                elif table_name4 in ('二级类目偏好'):
                     col_name4_3   = [ 'OPTION_L1' if x in ('所属一级类目') else 'PCT' if x in ('百分比') else 'OPTION_L2' if x in ('二级类目名称')  else x for x in list(row) if not pd.isnull(x)  ]
                elif table_name4 in ('叶子类目偏好'):
                     col_name4_4   = [ 'OPTION_L1' if x in ('所属一级类目') else 'PCT' if x in ('百分比') else 'OPTION_L2' if x in ('所属二级类目')  else 'OPTION_L3' if x in ('叶子类目名称')  else x  for x in list(row) if not pd.isnull(x)  ]
            elif rflag == 'r':
                 if   table_name4 in ('月均消费金额'):
                      arr4_1.append(tuple([x for x in row if not pd.isnull(x)]))
                 elif table_name4 in ('一级类目偏好'):
                      arr4_2.append(tuple([x for x in row if not pd.isnull(x)]))
                 elif table_name4 in ('二级类目偏好'):
                      arr4_3.append(tuple([x for x in row if not pd.isnull(x)]))
                 elif table_name4 in ('叶子类目偏好'):
                      arr4_4.append(tuple([x for x in row if not pd.isnull(x)]))
     
            p_ind   =  ind
            p_colid =  colid
            p_cttid =  cttid         

        pdf4_1 = pd.DataFrame(arr4_1 ,index = None,columns = col_name4_1) 
        pdf4_2 = pd.DataFrame(arr4_2 ,index = None,columns = col_name4_2)
        pdf4_3 = pd.DataFrame(arr4_3 ,index = None,columns = col_name4_3)
        pdf4_4 = pd.DataFrame(arr4_4 ,index = None,columns = col_name4_4)

        df4_1  = pd.concat([pd.DataFrame( np.repeat(segment_id,len(pdf4_1)),index = None,columns = ['SEGMENT_ID'] ),pdf4_1],axis =1 )  
        df4_2  = pd.concat([pd.DataFrame( np.repeat(segment_id,len(pdf4_2)),index = None,columns = ['SEGMENT_ID'] ),pdf4_2],axis =1 )       
        df4_3  = pd.concat([pd.DataFrame( np.repeat(segment_id,len(pdf4_3)),index = None,columns = ['SEGMENT_ID'] ),pdf4_3],axis =1 )      
        df4_4  = pd.concat([pd.DataFrame( np.repeat(segment_id,len(pdf4_4)),index = None,columns = ['SEGMENT_ID'] ),pdf4_4],axis =1 )  

        fdf4_1  = pd.concat([pd.DataFrame( np.repeat(401,len(df4_1)),index = None,columns = ['TAG_CD'] ),df4_1],axis =1 )  
        fdf4_2  = pd.concat([pd.DataFrame( np.repeat(402,len(df4_2)),index = None,columns = ['TAG_CD'] ),df4_2],axis =1 )       
        fdf4_3  = pd.concat([pd.DataFrame( np.repeat(403,len(df4_3)),index = None,columns = ['TAG_CD'] ),df4_3],axis =1 )      
        fdf4_4  = pd.concat([pd.DataFrame( np.repeat(404,len(df4_4)),index = None,columns = ['TAG_CD'] ),df4_4],axis =1 )  

        fdf4_1.to_sql('AliUnidesk_Temp', con=conn,if_exists='append' ,index=False,dtype=mapping_df_types(fdf4_1))
        fdf4_2.to_sql('AliUnidesk_Temp', con=conn,if_exists='append' ,index=False,dtype=mapping_df_types(fdf4_2))
        fdf4_3.to_sql('AliUnidesk_L2_Temp', con=conn,if_exists='replace' ,index=False,dtype=mapping_df_types(fdf4_3))
        fdf4_4.to_sql('AliUnidesk_L3_Temp', con=conn,if_exists='replace' ,index=False,dtype=mapping_df_types(fdf4_4))
        ##################################################################################table3#####################################
        secid      =0
        tblid      =0
        colid      =0
        p_colid    =0
        cttid      =0
        p_cttid    =0
        p_ind      =0
    
        table_name3 = ""
        col_name3_1   =list('')
        arr3_1 = []

        for index, row in table3.iterrows():
    
            cnt_nn = 0
            for i in range(len(tuple(row))):
                if  pd.isnull(tuple(row)[i]):
                    cnt_nn+= 1       
            ind =  len(tuple(row)) - cnt_nn

            if  ind !=0 :
                if ind == 1:
                    tblid =1
                else:
                    tblid =0
                    if  p_ind   ==  1 :
                        colid = 1
                    else:
                        colid = 0            
                    if  (p_colid == 1) or (p_cttid ==1):
                        cttid = 1
                    else:
                        cttid = 0          
                secid = 1
            else:        
                secid = 0
                tblid = 0
                colid = 0
                cttid = 0
        
            if   secid ==1 and tblid== 1:
                 rflag = 't'
            elif secid ==1 and colid== 1:
                 rflag = 'c'
            elif secid ==1 and cttid== 1:
                 rflag = 'r'
            else:
                 rflag = 'n'
            if   rflag == 't':
                 table_name3 = row[0]
            elif rflag == 'c':
                if   table_name3 in ('地域'):
                     col_name3_1   = [ 'OPTION' if x in ('选项') else 'PCT' if x in ('百分比') else x  for x in list(row) if not pd.isnull(x) ]
            elif rflag == 'r':
                 if   table_name3 in ('地域'):
                      arr3_1.append(tuple([x for x in row if not pd.isnull(x)])) 
            p_ind   =  ind
            p_colid =  colid
            p_cttid =  cttid         

        pdf3_1 = pd.DataFrame(arr3_1 ,index = None,columns = col_name3_1) 
        df3_1  = pd.concat([pd.DataFrame( np.repeat(segment_id,len(pdf3_1)),index = None,columns = ['SEGMENT_ID'] ),pdf3_1],axis =1 )
        fdf3_1  = pd.concat([pd.DataFrame( np.repeat(301,len(df3_1)),index = None,columns = ['TAG_CD'] ),df3_1],axis =1 )  
        fdf3_1.to_sql('AliUnidesk_Temp', con=conn,if_exists='append' ,index=False,dtype=mapping_df_types(fdf3_1))

        ##################################################################################table5#####################################
        secid      =0
        tblid      =0
        colid      =0
        p_colid    =0
        cttid      =0
        p_cttid    =0
        p_ind      =0

        table_name5 = ""

        col_name5_1   =list('')
        col_name5_2   =list('')
        col_name5_3   =list('')
        col_name5_4   =list('')
        col_name5_5   =list('')

        arr5_1 = []
        arr5_2 = []
        arr5_3 = []
        arr5_4 = []
        arr5_5 = []

        for index, row in table5.iterrows():
            cnt_nn = 0
            for i in range(len(tuple(row))):
                if  pd.isnull(tuple(row)[i]):
                    cnt_nn+= 1       
            ind =  len(tuple(row)) - cnt_nn
    
            if  ind !=0 :
                if ind == 1:
                    tblid =1
                else:
                    tblid =0
                    if  p_ind   ==  1 :
                        colid = 1
                    else:
                        colid = 0            
                    if  (p_colid == 1) or (p_cttid ==1):
                        cttid = 1
                    else:
                        cttid = 0          
                secid = 1
            else:        
                secid = 0
                tblid = 0
                colid = 0
                cttid = 0

            if   secid ==1 and tblid== 1:
                 rflag = 't'
            elif secid ==1 and colid== 1:
                 rflag = 'c'
            elif secid ==1 and cttid== 1:
                 rflag = 'r'
            else:
                 rflag = 'n'   
        
            if   rflag == 't':
                 table_name5 = row[0]
            elif rflag == 'c':
                if   table_name5 in ('生活习惯'):
                     col_name5_1   = [ 'OPTION' if x in ('选项') else 'PCT' if x in ('百分比') else x  for x in list(row) if not pd.isnull(x) ]
                elif table_name5 in ('电视剧风格'):
                     col_name5_2   = [ 'OPTION' if x in ('选项') else 'PCT' if x in ('百分比') else x  for x in list(row) if not pd.isnull(x) ]
                elif table_name5 in ('电影风格'):
                     col_name5_3   = [ 'OPTION' if x in ('选项') else 'PCT' if x in ('百分比') else x  for x in list(row) if not pd.isnull(x) ]
                elif table_name5 in ('音乐明星'):
                     col_name5_4   = [ 'OPTION' if x in ('选项') else 'PCT' if x in ('百分比') else x  for x in list(row) if not pd.isnull(x) ]
                elif table_name5 in ('综艺风格'):
                     col_name5_5   = [ 'OPTION' if x in ('选项') else 'PCT' if x in ('百分比') else x  for x in list(row) if not pd.isnull(x) ]
            elif rflag == 'r':
                 if   table_name5 in ('生活习惯'):
                      arr5_1.append(tuple([x for x in row if not pd.isnull(x)]))
                 elif table_name5 in ('电视剧风格'):
                      arr5_2.append(tuple([x for x in row if not pd.isnull(x)]))
                 elif table_name5 in ('电影风格'):
                      arr5_3.append(tuple([x for x in row if not pd.isnull(x)]))
                 elif table_name5 in ('音乐明星'):
                      arr5_4.append(tuple([x for x in row if not pd.isnull(x)]))
                 elif table_name5 in ('综艺风格'):
                      arr5_5.append(tuple([x for x in row if not pd.isnull(x)]))
     
            p_ind   =  ind
            p_colid =  colid
            p_cttid =  cttid         
  
        pdf5_1 = pd.DataFrame(arr5_1 ,index = None,columns = col_name5_1) 
        pdf5_2 = pd.DataFrame(arr5_2 ,index = None,columns = col_name5_2)
        pdf5_3 = pd.DataFrame(arr5_3 ,index = None,columns = col_name5_3)
        pdf5_4 = pd.DataFrame(arr5_4 ,index = None,columns = col_name5_4)
        pdf5_5 = pd.DataFrame(arr5_5 ,index = None,columns = col_name5_5)

        df5_1  = pd.concat([pd.DataFrame( np.repeat(segment_id,len(pdf5_1)),index = None,columns = ['SEGMENT_ID'] ),pdf5_1],axis =1 )  
        df5_2  = pd.concat([pd.DataFrame( np.repeat(segment_id,len(pdf5_2)),index = None,columns = ['SEGMENT_ID'] ),pdf5_2],axis =1 )       
        df5_3  = pd.concat([pd.DataFrame( np.repeat(segment_id,len(pdf5_3)),index = None,columns = ['SEGMENT_ID'] ),pdf5_3],axis =1 )      
        df5_4  = pd.concat([pd.DataFrame( np.repeat(segment_id,len(pdf5_4)),index = None,columns = ['SEGMENT_ID'] ),pdf5_4],axis =1 )  
        df5_5  = pd.concat([pd.DataFrame( np.repeat(segment_id,len(pdf5_5)),index = None,columns = ['SEGMENT_ID'] ),pdf5_5],axis =1 )  

        fdf5_1  = pd.concat([pd.DataFrame( np.repeat(501,len(df5_1)),index = None,columns = ['TAG_CD'] ),df5_1],axis =1 )  
        fdf5_2  = pd.concat([pd.DataFrame( np.repeat(502,len(df5_2)),index = None,columns = ['TAG_CD'] ),df5_2],axis =1 )       
        fdf5_3  = pd.concat([pd.DataFrame( np.repeat(503,len(df5_3)),index = None,columns = ['TAG_CD'] ),df5_3],axis =1 )      
        fdf5_4  = pd.concat([pd.DataFrame( np.repeat(504,len(df5_4)),index = None,columns = ['TAG_CD'] ),df5_4],axis =1 )  
        fdf5_5  = pd.concat([pd.DataFrame( np.repeat(505,len(df5_5)),index = None,columns = ['TAG_CD'] ),df5_5],axis =1 ) 

        fdf5_1.to_sql('AliUnidesk_Temp', con=conn,if_exists='append' ,index=False,dtype=mapping_df_types(fdf5_1))
        fdf5_2.to_sql('AliUnidesk_Temp', con=conn,if_exists='append' ,index=False,dtype=mapping_df_types(fdf5_2))
        fdf5_3.to_sql('AliUnidesk_Temp', con=conn,if_exists='append' ,index=False,dtype=mapping_df_types(fdf5_3))
        fdf5_4.to_sql('AliUnidesk_Temp', con=conn,if_exists='append' ,index=False,dtype=mapping_df_types(fdf5_4))
        fdf5_5.to_sql('AliUnidesk_Temp', con=conn,if_exists='append' ,index=False,dtype=mapping_df_types(fdf5_5))

    finally:
         os.remove(ud_path);

