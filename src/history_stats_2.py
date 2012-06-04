#!/bin/env python3

import os
import sys

if __name__=="__main__":

    limit = None
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
        if limit <= 0:
            limit = None

    history = {}
    hist_conf = os.path.expanduser("~/.bash_history")
    with open(hist_conf) as hfile:
        for line in hfile:
            if line[0] != "#":
                items = line.split()
                if len(items) > 0:

                    cmd = items[0]
                    history[cmd] = history.get(cmd,0) + 1

                    for j in range(len(items[1:])):
                        cmd = items[j]
                        if cmd in ("sudo", "|", "xargs"):
                            cmd = items[j]
                            history[cmd] = history.get(cmd,0) + 1
                            cmd = items[j+1]
                            history[cmd] = history.get(cmd,0) + 1


    stats = [ (history[cmd],cmd) for cmd in history ]

    stats.sort(reverse=True)

    for count,cmd in stats[0:limit]:
        print(count,"\t",cmd)
