Squid traffic counter script
======

1) About.

2) Requirements.

3) Installation.

4) Usage.

5) Copyright.

1) About.

This is a simple python script made to parse the squid log file and update the mysql database configured for this with the traffic used on per user bases. If the traffic limit is fully used then
the user is blocked. Also it can reset the traffic used when needed(usually on monthly bases). The script is optimized and the tests show that it can pars a 1 GB log file in 26-30 seconds on a
pretty slow-speed machine(only 2 GB RAM and a AMD Athlon(tm) II X2 220 Processor) with and IDE drive.

2) Requirements.

Python version 3.2.x with the pymysql package installed.
Squid installed with the ability to connect to the mysql database.

3) Installation.

First get the package from git:

git clone https://logicwreck@github.com/logicwreck/solutions.git -b squid_counter

Assuming that squid was installed under /usr/local/squid/, and python version 3.2 under /usr/local/bin/python3.2 the next steps will need to be taken:
 
 a) Put the squid db auth script(squid_db_auth) into the squid libexec directory, in this case it will be /usr/local/squid/libexec
 
 b) Put the squid configuration(squid.conf) into the /usr/local/squid/etc/ directory(or another directory that is used as the squid config directory)
 
 c) Create a database in mysql named squiddb, and assign it a user/password like:
 create database squiddb;
 GRANT ALL PRIVILEGES ON squiddb.* TO squid_user@localhost IDENTIFIED BY 'PASSWORD';
 flush privileges;
 
 d) Populate the squid database with the dump from squiddb.sql like:
 mysql -usquid_user -pPASSWORD squiddb < squiddb.sql
 
 e) Modify the line saying:
 auth_param basic program /usr/local/squid/libexec/squid_db_auth --user squid_user --password PASSWORD --md5 --persist
 in the squid configuration file to match the mysql squid user and password created.
 
 f) Launch Squid.
 
 g) Put the script itself(count_squidsql.py) into a directory from which you'll be running it, like into /root/traficcount_squid and configure the next lines there to match the correct mysql settings:
 login="squid_user"
 password="PASSWORD"
 database="squiddb"
 host_loc="localhost"
 h) Create the next cron jobs:
 * * * * * /root/traficcount_squid/count_squidsql.py -l /usr/local/squid/var/logs/access.log -a parse -s localhost
 0 * * * * /root/traficcount_squid/count_squidsql.py -l /usr/local/squid/var/logs/access.log -a rotate -s localhost
 0 0 1 * * /root/traficcount_squid/count_squidsql.py -l /usr/local/squid/var/logs/access.log -a reset -s localhost
 where the first will be the parsing of the squid log(note the log is /usr/local/squid/var/logs/access.log).
 the second will rotate the parsed log once per hour.
 the third will reset the traffic counters in the mysql database. 

4) Usage.

 Sample usage is:
 Usage:/root/traficcount_squid/count_squidsql.py --logfile/-l [LogFile Path] --action/-a [parse|rotate|reset] --server/-s [servername]
 Where the LogFile Path is the logfile to be parsed.
 The action is parse, rotate or reset where parse will parse the logfile, rotate will rotate the parsed logs and reset will reset the traffic counters.
 The servername is the server where squid is installed, this is done in order to manage more squid servers at once but needs additional configurations. The default will be localhost.

5) Copyright.

(The MIT License)

Copyright ¿ 2012 alpha_man (Valerian Martin), email: zacccp@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the .Software.), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED .AS IS., WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF 
OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
