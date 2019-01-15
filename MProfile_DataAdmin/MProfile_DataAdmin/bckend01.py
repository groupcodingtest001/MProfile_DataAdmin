
from   MProfile_DataAdmin.dmp_ud import dmp_ud
from   MProfile_DataAdmin.dmp_tc import dmp_tc
from   sqlalchemy import create_engine
import urllib
from   sqlalchemy import text
import os


def bckend01(i_sid,i_udpath,i_tcpath):
       #params = urllib.parse.quote_plus('DRIVER={ODBC Driver 13 for SQL Server};SERVER=(local) ;DATABASE=Test;DSN=(local);Trusted_Connection=yes')
       params = urllib.parse.quote_plus('DRIVER={ODBC Driver 13 for SQL Server};SERVER=52.80.196.236 ;DATABASE=mprofile_dev;UID=mprofile;PWD=mprofile_2018')
       conn = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params) 
       #conn = create_engine("mssql+pymssql://mprofile:mprofile_2018@52.80.196.236/mprofile_dev")
       try: 
           dmp_ud(i_sid,i_udpath);
           dmp_tc(i_sid,i_tcpath);
           conn.execute(text("EXEC SP_UD_ETL").execution_options(autocommit=True));
       except:
           conn_2 = conn.connect()
           conn_2.execute(text("UPDATE Segment_WD_Status SET Status = -1 WHERE DMP_ID in (2,5) and Segment_ID = :segmentid").execution_options(autocommit=True),segmentid=idv)
           conn_2.close()
       finally:
          os.remove(i_udpath);
          for file02_item in os.listdir(i_tcpath):
                os.remove(i_tcpath+'/'+file02_item);