Squid traffic counter script
======

1) About.<br />
2) Requirements.<br />
3) Installation.<br />
4) Usage.<br />
5) Copyright.<br />

1) About.<br />
This is a simple python script made to parse the squid log file and update the mysql database configured for this with the traffic used on per user bases. If the traffic limit is fully used then
the user is blocked. Also it can reset the traffic used when needed(usually on monthly bases). The script is optimized and the tests show that it can pars a 1 GB log file in 26-30 seconds on a
pretty slow-speed machine(only 2 GB RAM and a AMD Athlon(tm) II X2 220 Processor) with and IDE drive.

2) Requirements.<br />
Python version 3.2.x with the pymysql package installed.
Squid installed with the ability to connect to the mysql database.

3) Installation.<br />
First get the package from git:<br />
git clone https://logicwreck@github.com/logicwreck/solutions.git -b squid_counter<br />
or from our website:<br />
http://www.logicwreck.com/files/squid_counter-1.0.0.tar.gz<br />
after which you need to unarchive it(in case it was downloaded from our site) by running:<br />
tar xvfz squid_counter-1.0.0.tar.gz<br />

Assuming that squid was installed under /usr/local/squid/, and python version 3.2 under /usr/local/bin/python3.2 the next steps will need to be taken:<br />
 a) Put the squid db auth script(squid_db_auth) into the squid libexec directory, in this case it will be /usr/local/squid/libexec<br />
 b) Put the squid configuration(squid.conf) into the /usr/local/squid/etc/ directory(or another directory that is used as the squid config directory)<br />
 c) Create a database in mysql named squiddb, and assign it a user/password like:<br />
 create database squiddb;<br />
 GRANT ALL PRIVILEGES ON squiddb.* TO squid_user@localhost IDENTIFIED BY 'PASSWORD';<br />
 flush privileges;<br /> 
 d) Populate the squid database with the dump from squiddb.sql like:<br />
 mysql -usquid_user -pPASSWORD squiddb < squiddb.sql<br /> 
 e) Modify the line saying:<br />
 auth_param basic program /usr/local/squid/libexec/squid_db_auth --user squid_user --password PASSWORD --md5 --persist<br />
 in the squid configuration file to match the mysql squid user and password created.<br /> 
 f) Launch Squid.<br /> 
 g) Put the script itself(count_squidsql.py) into a directory from which you'll be running it, like into /root/traficcount_squid and configure the next lines there to match the correct mysql settings:<br />
 login="squid_user"<br />
 password="PASSWORD"<br />
 database="squiddb"<br />
 host_loc="localhost"<br />
 h) Create the next cron jobs:<br />
 * * * * * /root/traficcount_squid/count_squidsql.py -l /usr/local/squid/var/logs/access.log -a parse -s localhost<br />
 0 * * * * /root/traficcount_squid/count_squidsql.py -l /usr/local/squid/var/logs/access.log -a rotate -s localhost<br />
 0 0 1 * * /root/traficcount_squid/count_squidsql.py -l /usr/local/squid/var/logs/access.log -a reset -s localhost<br />
 where the first will be the parsing of the squid log(note the log is /usr/local/squid/var/logs/access.log).<br />
 the second will rotate the parsed log once per hour.<br />
 the third will reset the traffic counters in the mysql database.<br />

4) Usage.<br />
 Sample usage is:<br />
 Usage:/root/traficcount_squid/count_squidsql.py --logfile/-l [LogFile Path] --action/-a [parse|rotate|reset] --server/-s [servername]<br />
 Where the LogFile Path is the logfile to be parsed.<br />
 The action is parse, rotate or reset where parse will parse the logfile, rotate will rotate the parsed logs and reset will reset the traffic counters.<br />
 The servername is the server where squid is installed, this is done in order to manage more squid servers at once but needs additional configurations. The default will be localhost.<br />

5) Copyright.<br />
(The MIT License)<br />

Copyright © 2012 alpha_man (Valerian Martin), email: vmartin@logicwreck.com<br />

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the .Software.), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED .AS IS., WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF 
OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
