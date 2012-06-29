#!/usr/local/bin/python3.2

#import pymysql, sys, subprocess, shutil, pwd, grp, os, gzip, re, socket, urllib.request, random, string, tarfile, socket, struct, fcntl
import subprocess, sys, os, re, shutil, random, string, tarfile, pwd, grp 

class wp_migrate_class:
 def __init__(self):
  self.variables={}
  self.variables['rundir']=sys.path[0]+"/"
  self.variables['tmpdir']="/tmp/wp_tmp_"+self.random_string(10)
  self.variables['dumpcmd']="/usr/bin/mysqldump"
  self.variables['restorecmd']="/usr/bin/mysql"
  self.get_arguments()
  self.check_arguments()

 def action(self):
  if self.variables['action']==1:
   self.create_package()
  elif self.variables['action']==2:
   self.deploy_package()

 def create_package(self):
  self.make_tmp()
  self.get_site_url()
  self.precreate_package()
  self.tar_gzip_package()
  self.del_tmp()

 def deploy_package(self):
  self.make_tmp_deploy()
  self.predeploy_archive()
  self.deploy_get_vars()
  self.deploy_modify_dump()
  self.deploy_modify_wpconf()
  self.deploy_contents()
  self.del_tmp()

 def deploy_contents(self):
  if os.path.isdir(self.variables['wpdirectory']):
   self.copy_recursive_tree(self.variables['tmpdir']+"/wpdata/",self.variables['wpdirectory'])
  else:
   shutil.copytree(self.variables['tmpdir']+"/wpdata/", self.variables['wpdirectory'])
  if 'sysuser' in self.variables:
   if 'sysgroup' not in self.variables:
    self.variables['sysgroup']=self.variables['sysuser']
   self.chown_recursive(self.variables['wpdirectory'])
  outputz1=subprocess.check_output([self.variables['restorecmd']+" -u"+self.variables['wp_dbuser']+" -p"+self.variables['wp_dbpass']+" "+self.variables['wp_dbname']+" < "+self.variables['tmpdir']+"/wp_db.sql"], stderr=subprocess.STDOUT, shell=True)

 def predeploy_archive(self):
  pack_buf_name=re.sub('^.*\/','',self.variables['packagename'])
  tarz = tarfile.open(self.variables['packagename'])
  tarz.extractall(self.variables['tmpdir'])
  tarz.close() 

 def deploy_get_vars(self):
  WPSETTINGS = open(self.variables['tmpdir']+"/wp_settings.conf")
  buf_list = WPSETTINGS.readlines()
  if 'nsport' in self.variables:
   self.variables['destinationdomain']=self.variables['destinationdomain']+":"+self.variables['nsport']
  self.variables['destinationdomain']="http://"+self.variables['destinationdomain']
  for linea1 in buf_list:
   linea2=re.sub(r'\n','',linea1).split('=')
   if linea2[0] not in self.variables:
    self.variables[linea2[0]]=linea2[1]
   if linea2[0] == 'siteurl' and self.variables['destinationdomain'] == "http://example.com":
    self.variables['siteurl'] = linea2[1]
   elif linea2[0] == 'siteurl' and self.variables['destinationdomain'] != "http://example.com":
    self.variables['siteurl'] = self.variables['destinationdomain']
   del linea2
  del buf_list,linea1

 def deploy_modify_dump(self):
  try:
   WPSQLDump = open(self.variables['tmpdir']+"/wp_db.sql")
   buf_list = WPSQLDump.readlines()
   buf_write=""
   if self.variables['siteuri'] == "":
    self.variables['siteuri']="/"
   for linea1 in buf_list:
    modified_line=re.sub('<SITE_ROOT_DOC_HERE>',self.variables['wpdirectory'],linea1)
    modified_line=re.sub('<SITE_URI_NAME_HERE>',self.variables['siteuri'],modified_line)
    modified_line=re.sub('<SITE_URL_NAME_HERE>',self.variables['siteurl'],modified_line)
    buf_write+=modified_line
   WPSQLDump.close()
   WPSQLDump = open(self.variables['tmpdir']+"/wp_db.sql","w")
   WPSQLDump.write(buf_write)
   WPSQLDump.close()
   del buf_write,linea1,buf_list
  except IOError as err:
   print("I/O error: {0}".format(err))

 def deploy_modify_wpconf(self):
  try:
   WPConfigFile = open(self.variables['tmpdir']+"/wpdata/wp-config.php")
   buf_list = WPConfigFile.readlines()
   buf_write=""
   for linea1 in buf_list:
    line_buf=""
    if re.match("^.*DB_NAME.*$", linea1):
     line_buf=re.sub('^.*\'|^.*\"','',re.sub('^.*define\(.*DB_NAME.*,|\'\);.*$|\"\);.*$', '', linea1))
     line_buf=re.sub(r'\n','',line_buf)
     linea1=re.sub(line_buf,self.variables['wp_dbname'],linea1)
    elif re.match("^.*DB_USER.*$", linea1):
     line_buf=re.sub('^.*\'|^.*\"','',re.sub('^.*define\(.*DB_USER.*,|\'\);.*$|\"\);.*$', '', linea1))
     line_buf=re.sub(r'\n','',line_buf)
     linea1=re.sub(line_buf,self.variables['wp_dbuser'],linea1)
    elif re.match("^.*DB_PASSWORD.*$", linea1):
     line_buf=re.sub('^.*\'|^.*\"','',re.sub('^.*define\(.*DB_PASSWORD.*,|\'\);.*$|\"\);.*$', '', linea1))
     line_buf=re.sub(r'\n','',line_buf)
     linea1=re.sub(line_buf,self.variables['wp_dbpass'],linea1)
    elif re.match("^.*DB_HOST.*$", linea1):
     line_buf=re.sub('^.*\'|^.*\"','',re.sub('^.*define\(.*DB_HOST.*,|\'\);.*$|\"\);.*$', '', linea1))
     line_buf=re.sub(r'\n','',line_buf)
     linea1=re.sub(line_buf,self.variables['wp_dbhost'],linea1)
    del line_buf
    buf_write+=linea1
   WPConfigFile.close()
   WPConfigFile = open(self.variables['tmpdir']+"/wpdata/wp-config.php","w")
   WPConfigFile.write(buf_write)
   WPConfigFile.close()
   del buf_list,linea1,buf_write
  except IOError as err:
   print("I/O error: {0}".format(err))

 def del_tmp(self):
  shutil.rmtree(self.variables['tmpdir'])

 def tar_gzip_package(self):
  try:
   os.chdir(self.variables['tmpdir'])
   tarFilez = tarfile.open(self.variables['packagename'], mode = 'w:gz')
   tarFilez.add(".")
   tarFilez.close()
   os.chdir(self.variables['rundir'])
  except IOError as err:
   print("I/O error: {0}".format(err))

 def precreate_package(self):
  try:
   buf_write=""
   WPSQLDump = open(self.variables['tmpdir']+"/wp_db.sql")
   buf_list = WPSQLDump.readlines()
   if self.variables['siteuri'] == "":
    self.variables['siteuri']="/"
   for linea1 in buf_list:
    modified_line=re.sub(self.variables['siteurl'],'<SITE_URL_NAME_HERE>',linea1)
    modified_line=re.sub('<SITE_URL_NAME_HERE>'+self.variables['siteuri'],'<SITE_URL_NAME_HERE><SITE_URI_NAME_HERE>',modified_line)
    modified_line=re.sub(self.variables['wpdirectory'],'<SITE_ROOT_DOC_HERE>',modified_line)
    buf_write+=modified_line
   WPSQLDump.close()
   WPSQLDump = open(self.variables['tmpdir']+"/wp_db.sql","w")
   WPSQLDump.write(buf_write)
   WPSQLDump.close()
   buf_write="siteurl="+self.variables['siteurl']+"\n"
   buf_write+="siteuri="+self.variables['siteuri']+"\n"
   buf_write+="wp_dbname="+self.variables['wp_dbname']+"\n"
   buf_write+="wp_dbuser="+self.variables['wp_dbuser']+"\n"
   buf_write+="wp_dbpass="+self.variables['wp_dbpass']+"\n"
   buf_write+="wp_dbhost="+self.variables['wp_dbhost']+"\n"
   buf_write+="wpdirectory="+self.variables['wpdirectory']+"\n"
   WPSQLDump = open(self.variables['tmpdir']+"/wp_settings.conf","w")
   WPSQLDump.write(buf_write)
   WPSQLDump.close()
   del linea1, buf_list, buf_write
  except IOError as err:
   print("I/O error: {0}".format(err))

 def get_site_url(self):
  try:
   WPSQLDump = open(self.variables['tmpdir']+"/wp_db.sql")
   buf_list = WPSQLDump.readlines()
   for linea1 in buf_list:
    if re.match("^.*siteurl.*$", linea1):
     self.variables['siteurl']=re.sub('^.*siteurl\',\'|\',\'yes\'\).*$|\n','',linea1)
   WPSQLDump.close()
   del linea1, buf_list
  except IOError as err:
   print("I/O error: {0}".format(err))

 def make_tmp(self):
  self.get_wp_config_vars()
  os.mkdir(self.variables['tmpdir'])
  shutil.copytree(self.variables['wpdirectory'], self.variables['tmpdir']+"/wpdata")
  outputz1=subprocess.check_output([self.variables['dumpcmd']+" -u"+self.variables['wp_dbuser']+" -p"+self.variables['wp_dbpass']+" --routines "+self.variables['wp_dbname']+" > "+self.variables['tmpdir']+"/wp_db.sql"], stderr=subprocess.STDOUT, shell=True)

 def make_tmp_deploy(self):
  os.mkdir(self.variables['tmpdir'])

 def rm_tmp(self):
  shutil.rmtree(self.variables['tmpdir'])

 def random_string(self,length):
  return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(length))

 def get_wp_config_vars(self):
  try:
   WPConfigFile = open(self.variables['wpdirectory']+"/wp-config.php")
   buf_list = WPConfigFile.readlines()
   for linea1 in buf_list:
    if re.match("^.*DB_NAME.*$", linea1):
     self.variables['wp_dbname']=re.sub('^.*\'|^.*\"','',re.sub('^.*define\(.*DB_NAME.*,|\'\);.*$|\"\);.*$', '', linea1))
     self.variables['wp_dbname']=re.sub(r'\n','',self.variables['wp_dbname'])
    elif re.match("^.*DB_USER.*$", linea1):
     self.variables['wp_dbuser']=re.sub('^.*\'|^.*\"','',re.sub('^.*define\(.*DB_USER.*,|\'\);.*$|\"\);.*$', '', linea1))
     self.variables['wp_dbuser']=re.sub(r'\n','',self.variables['wp_dbuser'])
    elif re.match("^.*DB_PASSWORD.*$", linea1):
     self.variables['wp_dbpass']=re.sub('^.*\'|^.*\"','',re.sub('^.*define\(.*DB_PASSWORD.*,|\'\);.*$|\"\);.*$', '', linea1))
     self.variables['wp_dbpass']=re.sub(r'\n','',self.variables['wp_dbpass'])
    elif re.match("^.*DB_HOST.*$", linea1):
     self.variables['wp_dbhost']=re.sub('^.*\'|^.*\"','',re.sub('^.*define\(.*DB_HOST.*,|\'\);.*$|\"\);.*$', '', linea1))
     self.variables['wp_dbhost']=re.sub(r'\n','',self.variables['wp_dbhost'])
   WPConfigFile.close()
   del WPConfigFile, buf_list, linea1
  except IOError as err:
   print("I/O error: {0}".format(err))

 def get_arguments(self):
  i=0
  for argument in sys.argv:
   if sys.argv[i] == "--action" or sys.argv[i] == "-a":
    try:
     if sys.argv[i+1] == "package":
      self.variables['action']=1
     elif sys.argv[i+1] == "restore":
      self.variables['action']=2
    except:
     pass
   elif sys.argv[i] == "--directory" or sys.argv[i] == "-d":
    try:
     self.variables['wpdirectory']=sys.argv[i+1]
     self.variables['wpdirectory']=re.sub(r'\/$','',self.variables['wpdirectory'])
    except:
     pass
   elif sys.argv[i] == "--package" or sys.argv[i] == "-p":
    try:
     self.variables['packagename']=sys.argv[i+1]
     if not re.match("^\/", self.variables['packagename']):
      self.variables['packagename']=self.variables['rundir']+re.sub('^.*\/','',self.variables['packagename'])
    except:
     pass
   elif sys.argv[i] == "--siteuri" or sys.argv[i] == "-ur":
    try:
     self.variables['siteuri']=sys.argv[i+1]
     if not re.match("\/$", self.variables['siteuri']):       
      self.variables['siteuri']=self.variables['siteuri']+"/"
     if not re.match("^\/", self.variables['siteuri']):
      self.variables['siteuri']="/"+self.variables['siteuri']
    except:
     pass
   elif sys.argv[i] == "--systemuser" or sys.argv[i] == "-s":
    try:
     self.variables['sysuser']=sys.argv[i+1]
    except:
     pass
   elif sys.argv[i] == "--systemgroup" or sys.argv[i] == "-g":
    try:
     self.variables['sysgroup']=sys.argv[i+1]
    except:
     pass
   elif sys.argv[i] == "--dbuser" or sys.argv[i] == "-du":
    try:
     self.variables['wp_dbuser']=sys.argv[i+1]
    except:
     pass
   elif sys.argv[i] == "--dbpasswd" or sys.argv[i] == "-dp":
    try:
     self.variables['wp_dbpass']=sys.argv[i+1]
    except:
     pass
   elif sys.argv[i] == "--dbhost" or sys.argv[i] == "-dh":
    try:
     self.variables['wp_dbhost']=sys.argv[i+1]
    except:
     pass
   elif sys.argv[i] == "--dbname" or sys.argv[i] == "-dn":
    try:
     self.variables['wp_dbname']=sys.argv[i+1]
    except:
     pass
   elif sys.argv[i] == "--port" or sys.argv[i] == "-pt":
    try:
     self.variables['nsport']=sys.argv[i+1]
    except:
     pass
   elif sys.argv[i] == "--destination-domain" or sys.argv[i] == "-dd":
    try:
     self.variables['destinationdomain']=sys.argv[i+1]
    except:
     pass
   i+=1
  if not 'destinationdomain' in self.variables:
   self.variables['destinationdomain']="example.com"
   
 def check_arguments(self):
  if 'action' not in self.variables:
   self.print_usage()
   self.print_error(".........................")
   self.print_error("Error Code 1: No action specified.")
   sys.exit(1)
  if 'wpdirectory' not in self.variables or self.variables['wpdirectory']=="":
   self.print_usage()
   self.print_error(".........................")
   self.print_error("Error Code 2: No wordpress directory specified.")
   sys.exit(2)
  if 'packagename' not in self.variables or self.variables['packagename']=="":
   self.print_usage()
   self.print_error(".........................")
   self.print_error("Error Code 3: No package name specified.")
   sys.exit(3)   
  if self.variables['action'] == 1 and not os.path.isdir(self.variables['wpdirectory']):
   self.print_usage()
   self.print_error(".........................")
   self.print_error("Error Code 4: Wordpess directory given "+self.variables['wpdirectory']+" is not present!")
   sys.exit(4)
  if self.variables['action'] == 1 and not os.path.isfile(self.variables['wpdirectory']+"/wp-config.php"):
   self.print_usage()
   self.print_error(".........................")
   self.print_error("Error Code 5: Wordpess doesn't exist under "+self.variables['wpdirectory']+" !")
   sys.exit(5)
  if self.variables['action'] == 2 and not self.if_domain(self.variables['destinationdomain']):
   self.print_usage()
   self.print_error(".........................")
   self.print_error("Error Code 6: Destination domain "+self.variables['destinationdomain']+" is not a domain!")
   sys.exit(6)
  if self.variables['action'] == 2 and not os.path.isfile(self.variables['packagename']):
   self.print_usage()
   self.print_error(".........................")
   self.print_error("Error Code 7: Package not present")
   sys.exit(7)
  if self.variables['action'] == 2 and 'nsport' in self.variables:
   if not self.variables['nsport'].isdecimal() or re.match("^0", self.variables['nsport']):
    self.print_usage()
    self.print_error(".........................")
    self.print_error("Error Code 8: Non standard port must be a number.")
    sys.exit(8)
   elif int(self.variables['nsport']) > 65535:
    self.print_usage()
    self.print_error(".........................")
    self.print_error("Error Code 9: Port number too high, should be 65535 maximum.")
    sys.exit(9)
  if 'siteuri' not in self.variables:
   self.variables['siteuri'] = ""
   
 def if_domain(self,domain):
  if re.match(r'((?:(?:(?:[a-zA-Z0-9][\.\-_]?){0,62})[a-zA-Z0-9])+)\.([a-zA-Z0-9]{2,6})$', domain):
   return 1
  else:
   return 0
   
 def print_OK(self,stringz1):
  print("\033[92m"+stringz1+"\033[0m")

 def print_error(self,stringz1):
  print("\033[31m"+stringz1+"\033[0m")

 def print_status(self,stringz1):
  print("\033[33m"+stringz1+"\033[0m")

 def print_usage(self):
  self.print_error("usage: "+sys.argv[0]+" [--action/-a package,restore] [--directory/-d wp_directory] [--package/-p package_name] [--siteuri/-ur site URI, default /] [--systemuser/-s username] [--systemgroup/-g groupname] [--dbuser/-du username] [--dbpasswd/-dp password] [--dbhost/-dh host] [--dbname/-dn database] [--destination-domain/-dd domainname] [--port/-pt non-standard port]")
  self.print_OK("example: "+sys.argv[0]+" -a package -d /var/www/wordpress -p package_wordpress")
  self.print_OK(sys.argv[0]+" -a restore -d /var/www/wordpress -p package_wordpress -s wpusernew -du dbuser -dp dbpass")

 def get_list_dir_only(self,directory):
  return os.listdir(directory)

 def copy_recursive_tree(self,source,destination):
  for linea1 in self.get_list_dir_only(source):
   if os.path.isfile(destination+"/"+linea1) or os.path.islink(destination+"/"+linea1):
    os.remove(destination+"/"+linea1)
   elif os.path.isdir(destination+"/"+linea1):   
    shutil.rmtree(destination+"/"+linea1)
   if os.path.isfile(source+"/"+linea1):
    shutil.copy2(source+"/"+linea1, destination+"/"+linea1)
   elif os.path.isdir(source+"/"+linea1):
    shutil.copytree(source+"/"+linea1, destination+"/"+linea1)
  if os.path.isfile(source+"/.htaccess"):
   shutil.copytree(source+"/.htaccess", destination+"/.htaccess")
  del linea1

 def file_list_dir(self,directory):
  retval=[]
  for topdir, dirz, filez in os.walk(directory):
   for linea1 in filez:       
    retval.append(os.path.join(topdir, linea1))
   for linea1 in dirz:
    retval.append(os.path.join(topdir, linea1))
  del topdir, dirz, filez
  return retval

 def chown_recursive(self,directory):
  for linea1 in self.file_list_dir(directory):
   os.chown(linea1, pwd.getpwnam(self.variables['sysuser']).pw_uid, grp.getgrnam(self.variables['sysgroup']).gr_gid) 
  del linea1

 def __del__(self):
  del self.variables

work_obj=wp_migrate_class()
work_obj.action()
del work_obj
