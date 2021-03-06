#!/usr/bin/env python
import os

DIR_SOURCE = os.path.dirname(os.path.abspath(__file__))
DIR_WORKING = os.getcwd()

test_os = raw_input("Select OS Platform:\n[0] Linux\n[1] OSX\n> ")
test_which = raw_input("Would you like to benchmark current device, \
  or other device?\n[0] Current\n[1] Other\n> ")
test_label = raw_input("Please give this test a name\n> ")

if(test_which == str(0)):
  test_dev = "/tmp/test.dat"
elif(test_which == str(1)):
  test_dev = raw_input("Input block dev for test, eg. \"/dev/sdb:\n \
    *THIS WILL DESTORY ALL DATA ON DEVICE\n> ")
else:
  exit(1)

if(test_os == str(0)):
  dd_z2f_arg = "dd if=/dev/zero of=" + test_dev + " count=100 bs=256k oflag=direct 2>&1 | \
    grep bytes | sed 's,[a-zA-Z()/\,],,g' | \
    awk '{print $1/$3/1024/1024\" MB/s, \" 100/$3\" IOPS\"}'"

  dd_f2n_arg = "dd if=" + test_dev + " of=/dev/null count=100 bs=256k iflag=direct 2>&1 | \
    grep bytes | sed 's,[a-zA-Z()/\,],,g' | \
    awk '{print $1/$3/1024/1024\" MB/s, \" 100/$3\" IOPS\"}'"
elif(test_os == str(1)):
  dd_z2f_arg = "dd if=/dev/zero of=" + test_dev + " count=100 bs=256k 2>&1 | \
    grep bytes | sed 's,[a-zA-Z()/\,],,g' | \
    awk '{print $1/$2/1024/1024\" MB/s, \" 100/$2\" IOPS\"}'"

  dd_f2n_arg = "dd if=" + test_dev + " of=/dev/null count=100 bs=256k 2>&1 | \
    grep bytes | sed 's,[a-zA-Z()/\,],,g' | \
    awk '{print $1/$2/1024/1024\" MB/s, \" 100/$2\" IOPS\"}'"
else:
  exit(1)

fio_test_arg = "cat " + DIR_SOURCE + "/9417014/sdc_raw_libaio_direct.fio | sed 's/\/dev\/sdc/" + \
  test_dev.replace("/", "\/") + "/' | sed s/sdc/" + test_label.replace("/", "\/") + \
  "/ > /tmp/fio_test && fio /tmp/fio_test"

print fio_test_arg

con_or_abort = raw_input("Continue to test on device: {}?\n[0] ABORT\n[1] Continue\n> ".format(test_dev))

if(con_or_abort != str(1)):
  print "Aborting cleanly."
  exit(0)

#Start

dd_r2f_arg = "dd if=/dev/urandom of=/tmp/urandom_file bs=1048560 count=1024" #TODO: Make variable

dd_test_arg = "bash " + DIR_SOURCE + "/9416799/dd_test.sh /tmp/urandom_file " + test_dev

tmp = "Starting input: /dev/zero > output: {}".format(test_dev)
print tmp
dd_z2f_stdout = os.popen("echo \"" + tmp + "\" > dd_test.log").read()
dd_z2f_stdout = os.popen(dd_z2f_arg + " >> dd_test.log").read()
print dd_z2f_stdout

tmp = "Starting input: {} > output: /dev/null".format(test_dev)
print tmp
dd_z2f_stdout = os.popen("echo \"" + tmp + "\" >> dd_test.log").read()
dd_f2n_stdout = os.popen(dd_f2n_arg + " >> dd_test.log").read()
print dd_f2n_stdout

tmp = "Starting input: /dev/urandom > output: /tmp/urandom_file"
print tmp
dd_z2f_stdout = os.popen("echo \"" + tmp + "\" >> dd_test.log").read()
dd_r2f_stdout = os.popen(dd_r2f_arg + " >> dd_test.log").read() #FIX: NOT APPENDING
print dd_r2f_stdout

tmp = "Starting dd_test.sh: infile: /tmp/urandom_file outfile: {}".format(test_dev)
print tmp
dd_z2f_stdout = os.popen("echo \"" + tmp + "\" >> dd_test.log").read()
dd_test_stdout = os.popen(dd_test_arg + " >> dd_test.log").read()
print dd_test_stdout

print "Starting fio test: infile/outfile: {}".format(test_dev)
os.popen("mv /tmp/urandom_file /tmp/test.dat").read()
fio_test_stdout = os.popen(fio_test_arg).read() #Creates files in working dir
print fio_test_stdout
