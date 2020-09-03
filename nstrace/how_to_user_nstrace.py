#!/usr/bin/python3
import nstrace
import sys

def only_events(filename):
   nstrace.nsopen(filename)
   while not nstrace.isEOF():
       if nstrace.isEvent():
           (event, time, sendnode, dest, dummy, size,dummy, flow, dummy, dummy, dummy, dummy)=\
                nstrace.getEvent()
       else:
           nstrace.skipline()

def only_vars(file_name):
    nstrace.nsopen(file_name)
    while not nstrace.isEOF():
        if nstrace.isVar():
            (time, src_node, src_flow, dst_node, dst_flow, var_name, var_value)=\
                nstrace.getVar()
        else:
            nstrace.skipline()