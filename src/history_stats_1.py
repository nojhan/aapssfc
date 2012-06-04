#!/bin/env python3

import os

if __name__=="__main__":

    history = {}
    hist_conf = os.path.expanduser("~/.bash_history")
    with open(hist_conf) as hfile:
        for line in hfile:
            if line[0] != "#":
                items = line.split()
                if len(items) > 0:
                    cmd = items[0]

                    if cmd == "sudo":
                        history[cmd] = history.get(cmd,0) + 1
                        cmd = items[1]

                    history[cmd] = history.get(cmd,0) + 1


    stats = [ (history[cmd],cmd) for cmd in history ]

    stats.sort(reverse=True)

    for count,cmd in stats[0:30]:
        print(count,"\t",cmd)
