#!/bin/env python3

import os
import sys
import time
import subprocess

if __name__=="__main__":

    limit = None
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
        if limit <= 0:
            limit = None

    history = {}
    dates = {}
    hist_conf = os.path.expanduser("~/.bash_history")
    with open(hist_conf) as hfile:
        for line in hfile:
            if line[0] == "#":
                epoch = int(line[1:])
                t = time.localtime(epoch)
                (y,m,d,h) = (t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour)
                if y not in dates:
                    dates[y] = {}
                else:
                    if m not in dates[y]:
                        dates[y][m] = {}
                    else:
                        if d not in dates[y][m]:
                            dates[y][m][d] = {}
                        else:
                            if h not in dates[y][m][d]:
                                dates[y][m][d][h] = 0
                            else:
                                dates[y][m][d][h] += 1

            #elif line[0] != '"':
            else:

                items = line.split()
                if len(items) > 0:

                    cmd = os.path.basename(items[0])

                    history[cmd] = history.get(cmd,0) + 1

                    for j in range(len(items[1:])):
                        cmd = items[j]
                        if cmd in ("sudo", "|", "xargs"):
                            cmd = os.path.basename(items[j])
                            history[cmd] = history.get(cmd,0) + 1
                            cmd = os.path.basename(items[j+1])
                            history[cmd] = history.get(cmd,0) + 1

    stats = [ (history[cmd],cmd) for cmd in history ]

    stats.sort(reverse=True)

    for count,cmd in stats[0:limit]:
        with open("/dev/null","w") as dn:
            rcode = subprocess.call(["/bin/bash","-i","-c","type "+cmd+";exit"], stdout=dn, stderr=dn)
            if rcode == 0:
                print(count,"\t",cmd)


    hours = {}
    for y in dates:
        for m in dates[y]:
            for d in dates[y][m]:
                for h in dates[y][m][d]:
                    hours[h] = hours.get( h, 0 ) + 1
    smax = 4
    for h in hours:
        sh = " "*(smax-len(str(h)))
        print(h,end=sh)
    print()
    for h in hours:
        shh = " "*(smax-len(str(hours[h])))
        print(hours[h],end=shh)
    print()

