#!/usr/bin/env python
import os

# MACOSX: (SSD)
# dd if=/dev/zero of=/tmp/test.dat count=100 bs=256k 2>&1 | \
#       grep bytes | sed 's,[a-zA-Z()/],,g' | \
#       awk '{print $1/$2/1024/1024" MB/s "100/$2" IOPS"}'
# 507.11 MB/s 2028.44 IOPS
#
# dd of=/dev/null if=/tmp/test.dat count=100 bs=256k 2>&1 | \
#       grep bytes | sed 's,[a-zA-Z()/],,g' | \
#       awk '{print $1/$2/1024/1024" MB/s "100/$2" IOPS"}'
# 4994.01 MB/s 19976 IOPS

# LINUX:
# dd if=/dev/zero of=/tmp/test.dat count=100 bs=256k oflag=direct 2>&1 | \
#       grep bytes | sed 's,[a-zA-Z()/\,],,g' | \
#       awk '{print $1/$3/1024/1024" MB/s, " 100/$3" IOPS"}'
# 9.06885 MB/s, 36.2754 IOPS
#
# dd if=/tmp/test.dat of=/dev/null count=100 bs=256k iflag=direct 2>&1 | \
#       grep bytes | sed 's,[a-zA-Z()/\,],,g' | \
#       awk '{print $1/$3/1024/1024" MB/s, " 100/$3" IOPS"}'
# 48.6412 MB/s, 194.565 IOPS

test_os = raw_input("Select OS Platform:\n[0] Linux\n[1] OSX\n> ")
test_which = raw_input("Would you like to benchmark current device, \
  or other device?\n[0] Current\n[1] Other\n> ")

if(test_which == str(0)):
  test_dev = "/tmp/test.dat"
elif(test_which == str(1)):
  test_dev = raw_input("Input block dev for test, eg. \"/dev/sdb:\n \
    *THIS WILL DESTORY ALL DATA ON DEVICE\n> ")
else:
  exit(1)

con_or_abort = raw_input("Continue to test on device: {}?\n[0] ABORT\n[1] Continue\n> ".format(test_dev))

if(con_or_abort != str(1)):
  print "Aborting cleanly."
  exit(0)

#Start
print "Starting input: /dev/zero > output: {}".format(test_dev)
dd_z2f_arg = "dd if=/dev/zero of=" + test_dev + " count=100 bs=256k oflag=direct 2>&1 | \
  grep bytes | sed 's,[a-zA-Z()/\,],,g' | \
  awk '{print $1/$3/1024/1024\" MB/s, \" 100/$3\" IOPS\"}'"

dd_z2f_stdout = os.popen(dd_z2f_arg).read()
print dd_z2f_stdout
