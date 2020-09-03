#!/usr/bin/python3
import sys
import nstrace
import matplotlib.pyplot as plt

def only_vars(file_name, v_name):
    ts = []
    vs = []
    nstrace.nsopen(file_name)
    while not nstrace.isEOF():
        if nstrace.isVar():
            (time, src_node, src_flow, dst_node, dst_flow, var_name, var_value)=\
                nstrace.getVar()
            if v_name == var_name:
                ts.append(time)
                vs.append(var_value)
        else:
            nstrace.skipline()
    return ts, vs

ts, vs = only_vars('basic1.tr', 'cwnd_')
plt.plot(ts, vs)
plt.grid()
plt.xlabel('time')
plt.ylabel('cwnd')
plt.show()


