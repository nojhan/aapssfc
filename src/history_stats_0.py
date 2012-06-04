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
                    cmd = line.split()[0]

                    if cmd in history:
                        history[cmd] += 1
                    else:
                        history[cmd] = 1

    stats = []
    for cmd in history:
        stats.append( (history[cmd],cmd) )

    sort = sorted(stats, reverse=True)

    for count,cmd in sort[0:20]:
        print(count,"\t",cmd)
