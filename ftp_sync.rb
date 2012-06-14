#!/usr/bin/env ruby

require 'rubygems'
require 'fssm'
require 'optparse'
require 'net/ftp'

OPTS={}

def create_opts()
 retopts=""
 optparse = OptionParser.new do |opts|
  opts.banner = "Usage: #{$PROGRAM_NAME} [options]"
  OPTS[:directory] = nil
  opts.on( '-d', '--check-dir directory', 'Path to watched directory' ) do |directory|
   OPTS[:directory] = directory
  end
  OPTS[:server] = nil
  opts.on( '-s', '--ftp-server server', 'FTP server for uploads' ) do |server|
   OPTS[:server] = server
  end
  OPTS[:ftpuser] = nil
  opts.on( '-u', '--ftp-user user', 'FTP user to use' ) do |ftpuser|
   OPTS[:ftpuser] = ftpuser
  end
  OPTS[:ftppassword] = nil
  opts.on( '-p', '--ftp-pass password', 'FTP password to use' ) do |ftppassword|
   OPTS[:ftppassword] = ftppassword
  end
  opts.on( '-h', '--help', 'Show Help' ) do
   puts(opts)
   exit
  end
 retopts=opts
 end
 optparse.parse!
 return retopts
end

def check_options()
 opts_ret=create_opts()
 if OPTS[:directory] == nil
  puts("Directory #{OPTS[:directory]} option cannot be nil.")
  puts(opts_ret)
  exit
 end
 if not File.directory?(OPTS[:directory])
  puts("Directory #{OPTS[:directory]} is not present.")
  puts(opts_ret)
  exit
 end
 if OPTS[:server] == nil or OPTS[:ftpuser] == nil or OPTS[:ftppassword] == nil
  puts("FTP server and/or server login info not specified")
  puts(opts_ret)
  exit
 end
end

def file_open_wait(filename)
 initial_size=File.size?(filename)
 sleep(1)
 current_size=File.size?(filename)
 while initial_size!=current_size do
  initial_size=File.size?(filename)
  sleep(1)
  current_size=File.size?(filename)
 end
end

def ftp_upload(filetype="file",directory="/",filename="",passive="false")
 ftp=Net::FTP.open(OPTS[:server], user = OPTS[:ftpuser], passwd = OPTS[:ftppassword])
 ftp.passive = passive
 if filetype.to_s == "file"
  file_open_wait("#{OPTS[:directory]}/#{filename}")
  ftp.putbinaryfile("#{OPTS[:directory]}/#{filename}",filename.to_s)
 else
  ftp.mkdir(filename)
 end
 ftp.close()
end

def ftp_update(filetype="file",directory="/",filename="",passive="false")
 ftp=Net::FTP.open(OPTS[:server], user = OPTS[:ftpuser], passwd = OPTS[:ftppassword])
 ftp.passive = passive
 if filetype.to_s == "file"
  file_open_wait("#{OPTS[:directory]}/#{filename}")
  ftp.putbinaryfile("#{OPTS[:directory]}/#{filename}",filename.to_s)
 end
 ftp.close()
end

def ftp_delete(filetype="file",directory="/",filename="",passive="false")
 ftp=Net::FTP.open(OPTS[:server], user = OPTS[:ftpuser], passwd = OPTS[:ftppassword])
 ftp.passive = passive
 if filetype.to_s == "file"
  ftp.delete(filename)
 else
  ftp.rmdir(filename)
 end
 ftp.close()
end

check_options()
FSSM.monitor(OPTS[:directory], '**/*', :directories => true) do
 update do |root_dir_name, filename, filetype|
  ftp_update(filetype,"/",filename)
 end
 create do |root_dir_name, filename, filetype|
  ftp_upload(filetype,"/",filename)
 end
 delete do |root_dir_name, filename, filetype|
  ftp_delete(filetype,"/",filename)
 end
end