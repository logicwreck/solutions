AWS Billing script and Class documentation

1) About.
2) Requirements.
3) Installation.
4) Usage.
5) Copyright.

1) About.
This is a simple script used to synchronize the files and directories created/modified/deleted in a given directory on a linux box with an ftp server account.

2) Requirements.
Ruby version 1.8.7 or higher is required. The operating system should be Linux or FreeBSD as this was not tested on Windows.

3) Installation.
First the fssm gem needs to be installed by typing:
gem install fssm

Next you'll need to checkout the package from:
git clone https://github.com/logicwreck/solutions.git -b ftp_synchronize

After which you can move it to a location you want, like:
mv ftp_synchronize /opt/

4) Usage.
Sample usage command is:
Usage: ./ftp_sync.rb [options]
    -d, --check-dir directory        Path to watched directory
    -s, --ftp-server server          FTP server for uploads
    -u, --ftp-user user              FTP user to use
    -p, --ftp-pass password          FTP password to use
    -h, --help                       Show Help

Assuming that the package is located under /opt/ftp_synchronize a example usage would be:
/opt/ftp_synchronize/ftp_sync.rb -d /path/to/dir -s ftp.example.com -u example -p somepassword

5) Copyright.
(The MIT License)

Copyright © 2012 alpha_man (Valerian Martin), email: vmartin@logicwreck.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished 
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF 
OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
