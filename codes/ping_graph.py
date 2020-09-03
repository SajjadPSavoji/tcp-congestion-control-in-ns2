import os
import nstrace
import matplotlib.pyplot as plt
import random

def ping_parser(file_name):
    t1 = []
    v1 = []

    t2 = []
    v2 = []

    f = open(file_name, 'r')
    Lines = f.readlines()

    for i in range(len([line for line in Lines]) - 1):
        try:
            lne1 = Lines[i].split()
            lne2 = Lines[i+1].split()
            
            if lne1[0] == "node":
                source_node = int(lne1[1])
                time = float(lne2[2])
                ping = float(lne2[8])

                if source_node == 0:
                    t1.append(time)
                    v1.append(ping)
                elif source_node == 1:
                    t2.append(time)
                    v2.append(ping)

            else:
                pass
        except:
            pass
    return t1, v1, t2, v2


def find_index(t, sec):
    for i in range(len(t)):
        if i > sec:
            return i - 1
    return int(i)

filename = 'main.tcl'
agents = ['Agent/TCP', 'Agent/TCP/Newreno', 'Agent/TCP/Vegas']
ftr_name = 'ping.txt'
fnm_name = 'test.nam'
many = 5

plt.figure(figsize=(20, 20))

for agent in agents:

    t0s = []
    v0s = []
    t1s = []
    v1s = []
    for i in range(many):
        n23_d = str(int(random.uniform(5, 25))) + 'ms'
        n46_d = str(int(random.uniform(5, 25))) + 'ms'

        os.system(f'ns {filename} {agent} {n23_d} {n46_d} {ftr_name} {fnm_name}')
        t0, v0, t1, v1 = ping_parser(ftr_name)
        t0s.append(t0)
        t1s.append(t1)
        v0s.append(v0)
        v1s.append(v1)

    T0, V0, T1, V1 = [], [], [], []
    
    max_time = -1
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

plt.title(f'PING(avg on {many} times)')
plt.grid()
plt.legend()
plt.xlabel('time(s)')
plt.ylabel('avg ping')
plt.show()


# import os
# import nstrace
# import matplotlib.pyplot as plt
# import random

# def only_vars(file_name, v_name):
#     t1 = []
#     v1 = []

#     t2 = []
#     v2 = []

#     nstrace.nsopen(file_name)
#     while not nstrace.isEOF():
#         if nstrace.isVar():
#             (time, src_node, src_flow, dst_node, dst_flow, var_name, var_value)=\
#                 nstrace.getVar()
#             if v_name == var_name:
#                 if src_node == 0:
#                     t1.append(time)
#                     v1.append(var_value)
#                 elif src_node == 1:
#                     t2.append(time)
#                     v2.append(var_value)
#         else:
#             nstrace.skipline()
#     nstrace.nsclose()
#     return t1, v1, t2, v2


# def all_done(ptrs, txs):
#     for i in range(len(ptrs)):
#         if not ptrs[i] == (len(txs[i])-1):
#             return False
#     return True

# def arg_min(txs, ptrs):
#     mn = float('inf')
#     mn_idx = -1
#     for i in range(len(ptrs)):
#         if (txs[i][ptrs[i]] < mn) and (not ptrs[i] == len(txs[i])-1):
#             mn = txs[i][ptrs[i]]
#             mn_idx = i
#     return mn_idx, mn

# def inc(txs, ptrs, mn):
#     for i in range(len(ptrs)):
#         if txs[i][ptrs[i]] == mn:
#             if not ptrs[i]==len(txs[i])-1:
#                 ptrs[i] += 1

# def avg(txs, ptrs):
#     sum = 0
#     for i in range(len(ptrs)):
#         if ptrs[i] == 0 or ptrs[i] == len(txs[i])-1:
#             sum += txs[i][ptrs[i]]
#         else:
#             sum += txs[i][ptrs[i]-1]
#     return sum/len(ptrs)

# filename = 'main.tcl'
# agents = ['Agent/TCP', 'Agent/TCP/Newreno', 'Agent/TCP/Vegas']
# ftr_name = 'test.tr'
# fnm_name = 'test.nam'
# many = 1
# step = 1


# plt.figure(figsize=(20, 20))

# for agent in agents:

#     t0s = []
#     v0s = []
#     t1s = []
#     v1s = []
#     for i in range(many):
#         n23_d = str(int(random.uniform(5, 25))) + 'ms'
#         n46_d = str(int(random.uniform(5, 25))) + 'ms'

#         os.system(f'ns {filename} {agent} {n23_d} {n46_d} {ftr_name} {fnm_name}')
#         t0, v0, t1, v1 = only_vars(ftr_name, 'rtt_')
#         t0s.append(t0)
#         t1s.append(t1)
#         v0s.append(v0)
#         v1s.append(v1)
    
#     print(t0s, v0s)
#     T0, V0, T1, V1 = [], [], [], []
#     ptrs = [0 for i in range(many)]

#     while(not all_done(ptrs, t0s)):
#         mn_idx , mn = arg_min(t0s, ptrs)
#         T0.append(mn)
#         V0.append(avg(v0s, ptrs))
#         inc(t0s, ptrs, mn)

#     ptrs = [0 for i in range(many)]

#     while(not all_done(ptrs, t1s)):
#         mn_idx , mn = arg_min(t1s, ptrs)
#         T1.append(mn)
#         V1.append(avg(v1s, ptrs))
#         inc(t1s, ptrs, mn)

#     plt.plot(T0[::step], V0[::step], label=f'flow0 :: {agent}')
#     plt.plot(T1[::step], V1[::step], label=f'flow1 :: {agent}')

# plt.title(f'RTT(avg on {many} times)')
# plt.grid()
# plt.legend()
# plt.xlabel('time(s)')
# plt.ylabel('avg rtt_')
# plt.show()