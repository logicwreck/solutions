Wordpress migration script
=======
1) About.<br />
2) Requirements.<br />
3) Installation.<br />
4) Usage.<br />
5) Copyright.<br />

1) About.<br />

This is a simple python script made to package a wordpress site under a given directory and then unpack it into another directory(could be on another server) in a manner that it works correctly
afterwards. In two words it's a script made to migrate wordpress made sites from one server to another in two clicks.

2) Requirements.<br />
Python version 3.2.x<br />
mysqldump and mysql binaries present under /usr/bin/ , otherwise there will be a need to modify the self.variables['dumpcmd'] and self.variables['restorecmd'] variables in the script by pointing
to the correct locations.

3) Installation.<br />
You'll need to checkout the package from:<br />
git clone https://github.com/logicwreck/solutions.git -b wp_migration<br />
or from our website:<br />
http://www.logicwreck.com/files/wp_migration-1.0.0.zip<br />
after which you need to unarchive it(in case it was downloaded from our site) by running:<br />
unzip wp_migration-1.0.0.zip<br />

Just put it into some directory from where you'll be able to run easily run it.<br />

4) Usage.<br />
Sample usage is:<br />
usage: /root/wp_migration/migration.py [--action/-a package,restore] [--directory/-d wp_directory] [--package/-p package_name] [--siteuri/-ur site URI, default /] [--systemuser/-s username] [--systemgroup/-g groupname] [--dbuser/-du username] [--dbpasswd/-dp password] [--dbhost/-dh host] [--dbname/-dn database] [--destination-domain/-dd domainname] [--port/-pt non-standard port]<br />
Where:<br />
a) --action/-a - shows either to package the wordpress installation from a directory or restore it into the given directory.<br />
b) --directory/-d - the directory which will be packaged or the directory where the package will be restored.<br />
c) --package/-p - the package name to use for either packaging or restoring the wp installation.<br />
d) --siteuri/-ur - the URI that is being used, like example.com/wordpress/is/here will have the URI /wordpress/is/here<br />
e) --systemuser/-s - system user to be used for chowning the restored data to.<br />
f) --systemgroup/-g - system group to be used for chowning the restored data to.<br />
g) --dbuser/-du - database user to be used for mysql for the restored package if not like the initial.<br />
h) --dbpasswd/-dp - database password to be used for mysql for the restored package if not like the initial.<br />
k) --dbhost/-dh - database host to be used for mysql for the restored package if not like the initial.<br />
l) --dbname/-dn - database name to be used for mysql for the restored package if not like the initial.<br />
m) --destination-domain/-dd - the destination domain name to be used in case it's not like the original.<br />
n) --port/-pt non-standard - non-standard port where the web server listens in case it's not 80 or 443.<br />

5) Copyright.<br />
(The MIT License)<br />

Copyright © 2012 alpha_man (Valerian Martin), email: zacccp@gmail.com<br />

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished 
to do so, subject to the following conditions:<br />

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.<br />

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF 
OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.