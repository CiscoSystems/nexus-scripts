#
# Author: Arvind Somya (asomya@cisco.com)
#
#!/usr/bin/python

import os
import re
import subprocess
import time

sub = '10.%s.%s.0'
net = 'net%s%s'

subs = []
nets = []
srt = 0
end = 255

for k in range(0, 2):
    for i in range(srt, end):
        lsub =  sub % (k, i)
        lnet = net % (k, i)

        cmd1 = "quantum net-create %s" % lnet
        os.system(cmd1)
        nets.append(lnet)
        cmd2 = ["quantum", "subnet-create", lnet, "%s/24" % lsub]
        op = subprocess.Popen(cmd2, stdout = subprocess.PIPE).communicate()[0]
        sid = ''
        for line in op.splitlines():
            m = re.match(r"\| id\.*", line)
            if m:
                spl = [sp.strip() for sp in line.split('|') if sp != '']
                sid = spl[1]
                subs.append(sid)
        cmd3 = ["quantum","router-interface-add","r1",sid]
        subprocess.Popen(cmd3)

time.sleep(10)
val = raw_input("\n\nPress any key to start deleting:")

for sid in subs:
    cmd = ["quantum","router-interface-delete","r1",sid]
    subprocess.Popen(cmd)

for lnet in nets:
    cmd = "quantum net-delete %s" % lnet
    os.system(cmd)
