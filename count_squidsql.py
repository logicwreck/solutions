#!/usr/local/bin/python3.2

import pymysql, sys, subprocess, shutil, pwd, grp, os, gzip

login="squid_user"
password="squid_password"
database="squiddb"
host_loc="localhost"

class SquidParseClass:
 def __init__(self):
  self.trafficcur={}
  self.trafficmax={}
  self.trafficover={}
  self.logfile=""
  self.action=0
  self.server=""
  self.valid=0
  try:
   self.conn = pymysql.connect(host=host_loc, port=3306, user=login, passwd=password, db=database)
   self.cur = self.conn.cursor()
  except Exception as e:
   print("Error Occured: %s", e)
   raise
  if len(sys.argv) < 7:
   print("Usage:"+sys.argv[0]+" --logfile/-l [LogFile Path] --action/-a [parse|rotate|reset] --server/-s [servername]")
   sys.exit(1)
  i=0
  flag=0
  for argument in sys.argv:
   if sys.argv[i] == "--logfile" or sys.argv[i] == "-l":
    if not os.path.isfile(sys.argv[i+1]):
     print("Log file not present in the specified path or not a file")
     sys.exit(2)
    else:
     self.logfile=sys.argv[i+1]
     flag+=1
   if sys.argv[i] == "--server" or sys.argv[i] == "-s":
    self.server=sys.argv[i+1]
    self.cur.execute("select ID,MySQL_user,MySQL_password from squid_servers where ServerName='"+self.server+"';")
    self.server=self.cur.fetchall()[0]
    if not self.server:
     print("No such server present")
     sys.exit(3)     
    else:
     self.cur.execute("select user,band_used,band_max,allow_overuse from squid_traffic where serverid='"+str(self.server[0])+"';")
     resultz=self.cur.fetchall()
     for result1 in resultz:
      self.trafficcur[result1[0]]=result1[1]
      self.trafficmax[result1[0]]=result1[2]
      self.trafficover[result1[0]]=result1[3]
     self.trafficcur["-"]=0
     del resultz, result1
     flag+=1
   if sys.argv[i] == "--action" or sys.argv[i] == "-a":
    if sys.argv[i+1] == "parse":
     self.action=1
     flag+=1
    elif sys.argv[i+1] == "rotate":
     self.action=2
     flag+=1
    elif sys.argv[i+1] == "reset":
     self.action=3
     flag+=1
    else:
     print("Action must be parse or rotate")
     sys.exit(3)
   i+=1
  if flag is 3:
   self.valid=1
  del i, flag  

 def query(self, mySQLquery):
   try:
    self.cur.execute(mySQLquery)
   except Exception as e:
    print("Error Occured: %s", e)
    raise

 def GetResults(self):
  self.ret_val = self.cur.fetchall()
  return self.ret_val

 def ParseLog(self):
  pwdz = pwd.getpwnam("squid")
  squid_uid = pwdz.pw_uid
  grpz = grp.getgrnam('squid')
  squid_gid = grpz.gr_gid
  del grpz, pwdz
  try:
   FILE = open(self.logfile)
   FILE_backup=open(self.logfile+".processed",'a');
   for linez1 in FILE:
    FILE_backup.write(linez1);
    linez2=linez1.split()
    self.trafficcur[linez2[7]]+=int(linez2[1])
    del linez1, linez2
   FILE.close()
   FILE_backup.close()
   del FILE, FILE_backup
   query_traf="update squidpasswd set enabled='0' where "
   query_user=""
   for traf_id in self.trafficcur:
    if traf_id!="-":
     query_user+="update squid_traffic set band_used='"+str(self.trafficcur[traf_id])+"' where user='"+traf_id+"' and serverid='"+str(self.server[0])+"';"
     if self.trafficcur[traf_id] > self.trafficmax[traf_id] and not self.trafficover[traf_id] and self.trafficmax[traf_id] != 0:
      if len(query_traf) is 41:
       query_traf+="user='"+traf_id+"' "
      else:
       query_traf+="AND user="+traf_id+"' "
   query_traf+=";"
   if len(query_user) > 0:
    self.cur.execute(query_user)
   if len(query_traf) > 42:
    self.cur.execute(query_traf) 
    try:
     conn1 = pymysql.connect(host=host_loc, port=3306, user=login, passwd=password, db=database)
     cur1 = self.conn.cursor()
     cur1.execute(query_traf)
     cur1.close()
     conn1.close()
     del conn1,cur1
    except Exception as e:
     print("Error Occured: %s", e)
     raise
   del query_traf, query_user, traf_id
   FILE = open(self.logfile,"w")
   FILE.close()
   del FILE
  except IOError as err:
   print("I/O error: {0}".format(err))
  except:
   print("Error: Cannot manipulate temporary logfile - ", sys.exc_info()[0])
   raise
 
 def RotateLog(self,files):
  if str.isdigit(str(files)):
   if os.path.isfile(self.logfile+".processed."+str(files)+".gz"):
    os.remove(self.logfile+".processed."+str(files)+".gz")
   files-=1
   while (files > 0):
    if os.path.isfile(self.logfile+".processed."+str(files)+".gz"):
     shutil.move(self.logfile+".processed."+str(files)+".gz",self.logfile+".processed."+str(files+1)+".gz")
    files-=1
   FILE = open(self.logfile+".processed")
   GZIPED = gzip.GzipFile(filename=self.logfile+".processed.1.gz", mode='wb', compresslevel=9)
   for linez1 in FILE:
    GZIPED.write(linez1.encode('utf-8'))
   FILE.close()
   GZIPED.close()
   FILE = open(self.logfile+".processed","w")
   FILE.close()
   del FILE,GZIPED,linez1
   return 1
  else:
   return 0

 def ResetCounter(self):
  self.cur.execute("update squid_traffic set band_used='0' where serverid='"+str(self.server[0])+"';")
 
 def __del__(self):
  self.cur.close()
  self.conn.close()
  del self.trafficcur, self.trafficmax, self.trafficover, self.cur, self.conn, self.logfile, self.valid, self.action, self.server

parserz=SquidParseClass()
if parserz.valid:
 if parserz.action == 1:
  parserz.ParseLog()
 elif parserz.action == 2:
  parserz.RotateLog(5)
 elif parserz.action == 3:
  parserz.ResetCounter()
del parserz
