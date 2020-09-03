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

def all_done(ptrs, txs):
    for i in range(len(ptrs)):
        if not ptrs[i] == (len(txs[i])-1):
            return False
    return True

def arg_min(txs, ptrs):
    mn = float('inf')
    mn_idx = -1
    for i in range(len(ptrs)):
        if (txs[i][ptrs[i]] < mn) and (not ptrs[i] == len(txs[i])-1):
            mn = txs[i][ptrs[i]]
            mn_idx = i
    return mn_idx, mn

def inc(txs, ptrs, mn):
    for i in range(len(ptrs)):
        if txs[i][ptrs[i]] == mn:
            if not ptrs[i]==len(txs[i])-1:
                ptrs[i] += 1

def avg(txs, ptrs):
    sum = 0
    for i in range(len(ptrs)):
        if ptrs[i] == 0 or ptrs[i] == len(txs[i])-1:
            sum += txs[i][ptrs[i]]
        else:
            sum += txs[i][ptrs[i]-1]
    return sum/len(ptrs)

def to_end(T, V, end_time=1000):
    tf = T[-1]
    vf = V[-1]
    while(tf < end_time):
        tf += 1
        T.append(tf)
        V.append(vf)


filename = 'main.tcl'
agents = ['Agent/TCP', 'Agent/TCP/Newreno', 'Agent/TCP/Vegas']
ftr_name = 'test.tr'
fnm_name = 'test.nam'
many = 10
step = 20
packet_size = 1000*8 #bit
th_band = 100*1000 #bit/sec
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
        t0, v0, t1, v1 = only_vars(ftr_name, 'maxseq_')
        t0s.append(t0)
        t1s.append(t1)
        v0s.append(v0)
        v1s.append(v1)


    T0, V0, T1, V1 = [], [], [], []
    ptrs = [0 for i in range(many)]

    while(not all_done(ptrs, t0s)):
        mn_idx , mn = arg_min(t0s, ptrs)
        T0.append(mn)
        V0.append(avg(v0s, ptrs))
        inc(t0s, ptrs, mn)

    ptrs = [0 for i in range(many)]

    while(not all_done(ptrs, t1s)):
        mn_idx , mn = arg_min(t1s, ptrs)
        T1.append(mn)
        V1.append(avg(v1s, ptrs))
        inc(t1s, ptrs, mn)
    
    for index, maxseq in enumerate(V0):
        if T0[index] == 0 :
            V0[index] = 0
        else:
            V0[index] = (V0[index]+1)*packet_size/(T0[index] * th_band)

    for index, maxseq in enumerate(V1):
        if T1[index] == 0:
            V1[index] = 0
        else:
            V1[index] = (V1[index]+1)*packet_size/(T1[index] * th_band)
    
    to_end(T0, V0, end_time)
    to_end(T1, V1, end_time)

    step = round(len(T0)/end_time)
    plt.plot(T0[::step], V0[::step], label=f'flow0 :: {agent}')
    step = round(len(T1)/end_time)
    plt.plot(T1[::step], V1[::step], label=f'flow1 :: {agent}')

plt.title(f'goodput(avg on {many} times)')
plt.grid()
plt.legend()
plt.xlabel('time(s)')
plt.ylabel('goodput')
plt.show()