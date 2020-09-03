import os
import nstrace
import matplotlib.pyplot as plt
import random

def only_vars(file_name, v_name):
    t1 = []
    v1 = []

    t2 = []
    v2 = []

    nstrace.nsopen(file_name)
    while not nstrace.isEOF():
        if nstrace.isVar():
            (time, src_node, src_flow, dst_node, dst_flow, var_name, var_value)=\
                nstrace.getVar()
            if v_name == var_name:
                if src_node == 0:
                    t1.append(time)
                    v1.append(var_value)
                elif src_node == 1:
                    t2.append(time)
                    v2.append(var_value)
        else:
            nstrace.skipline()
    nstrace.nsclose()
    return t1, v1, t2, v2


def find_index(t, sec):
    index = -1
    for i in t:
        if int(i) < sec :
            index += 1
        if int(i) > sec:
            break
    return index

filename = 'main.tcl'
agents = ['Agent/TCP', 'Agent/TCP/Newreno', 'Agent/TCP/Vegas']
ftr_name = 'test.tr'
fnm_name = 'test.nam'
many = 10
max_time = -1
end_time = 1000


plt.figure(figsize=(20, 20))

for agent in agents:

    t0s = []
    v0s = []
    t1s = []
    v1s = []
    for i in range(many):
        n23_d = str(int(random.uniform(5, 25))) + 'ms'
        n46_d = str(int(random.uniform(5, 25))) + 'ms'

        os.system(f'ns {filename} {agent} {n23_d} {n46_d} {ftr_name} {fnm_name} {end_time}')
        t0, v0, t1, v1 = only_vars(ftr_name, 'rtt_')
        t0s.append(t0)
        t1s.append(t1)
        v0s.append(v0)
        v1s.append(v1)
    
    T0, V0, T1, V1 = [], [], [], []

    for i in t0s:
        max_time = max(max_time, int(max(i)))

    for sec in range(max_time):    
        T0.append(sec)
        v0 = 0
        for times in range(many):
            index = find_index(t0s[times], sec)
            v0 += v0s[times][index]
        V0.append(v0 / many)

    for sec in range(max_time):    
        T1.append(sec)
        v1 = 0
        for times in range(many):
            index = find_index(t1s[times], sec)
            v1 += v1s[times][index]
        V1.append(v1 / many)


    plt.plot(T0, V0, label=f'flow0 :: {agent}')
    plt.plot(T1, V1, label=f'flow1 :: {agent}')

plt.title(f'RTT(avg on {many} times)')
plt.grid()
plt.legend()
plt.xlabel('time(s)')
plt.ylabel('avg rtt_')
plt.show()