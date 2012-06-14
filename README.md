AWS Billing script and Class documentation
=======
1) About.<br />
2) Requirements.<br />
3) Installation.<br />
4) Usage.<br />
5) Copyright.<br />

1) About.<br />
This is a simple script used to synchronize the files and directories created/modified/deleted in a given directory on a linux box with an ftp server account.<br />

2) Requirements.<br />
Ruby version 1.8.7 or higher is required. The operating system should be Linux or FreeBSD as this was not tested on Windows.<br />

3) Installation.<br />
First the fssm gem needs to be installed by typing:<br />
gem install fssm<br />

Next you'll need to checkout the package from:<br />
git clone https://github.com/logicwreck/solutions.git -b ftp_synchronize<br />

After which you can move it to a location you want, like:<br />
mv ftp_synchronize /opt/<br />

4) Usage.<br />
Sample usage command is:<br />
Usage: ./ftp_sync.rb [options]<br />
    -d, --check-dir directory        Path to watched directory<br />
    -s, --ftp-server server          FTP server for uploads<br />
    -u, --ftp-user user              FTP user to use<br />
    -p, --ftp-pass password          FTP password to use<br />
    -h, --help                       Show Help<br />

Assuming that the package is located under /opt/ftp_synchronize a example usage would be:<br />
/opt/ftp_synchronize/ftp_sync.rb -d /path/to/dir -s ftp.example.com -u example -p somepassword<br />

5) Copyright<br />
(The MIT License)<br />

Copyright © 2012 alpha_man (Valerian Martin), email: vmartin@logicwreck.com<br />

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished 
to do so, subject to the following conditions:<br />

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.<br />

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF 
OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.