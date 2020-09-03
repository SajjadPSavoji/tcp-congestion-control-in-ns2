import os
import nstrace
import matplotlib.pyplot as plt
import random
import numpy as np

def drop_parser(file_name, v_name):
    t1 = []

    t2 = []

    f = open(file_name, 'r')
    Lines = f.readlines()

    for i in range(len([line for line in Lines]) - 1):
        try:
            lne = Lines[i].split()
            flag = lne[0]
            if flag == v_name:
                source_node = int(lne[7])
                time = float(lne[1])

                if source_node == 0:
                    t1.append(time)

                elif source_node == 1:
                    t2.append(time)


            else:
                pass
        except:
            pass
    
    f.close()
    return t1,t2

def make_v(t, max_time):
    v = []
    for time in range(max_time):
        num = 0
        for i in t:
            if i < time:
                pass
            elif i > time + 1:
                pass
            else:
                num += 1
        v.append(num)

    return v


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

    t1s = []

    for i in range(many):
        random.seed(5)
        n23_d = str(int(random.uniform(5, 25))) + 'ms'
        n46_d = str(int(random.uniform(5, 25))) + 'ms'

        os.system(f'ns {filename} {agent} {n23_d} {n46_d} {ftr_name} {fnm_name} {end_time}')
        t0, t1 = drop_parser(ftr_name, 'd')
        t0s.append(t0)   
        t1s.append(t1)

    if t0s[0] == []:
        plt.plot([0, end_time], [0, 0], label=f'flow0 :: {agent}')
        plt.plot([0, end_time], [0, 0], label=f'flow1 :: {agent}')
        continue
    for i in t0s:
        max_time = max(max_time, int(max(i)))


    v0s = [make_v(t0s[i], max_time) for i in range(many)]
    v1s = [make_v(t1s[i], max_time) for i in range(many)]
    # print(v0s, v1s)
    V0, V1 = [], []
    for i in range(len(v0s[0])):
        v = 0
        for j in range(many): 
            v += v0s[j][i]
        V0.append(v / many)


    for i in range(len(v1s[0])):
        v = 0
        for j in range(many): 
            v += v1s[j][i]
        V1.append(v / many)

    # print("_______")
    # print(V0)
    # print(V1)
    V0 = [sum(V0[:i]) / i for i in range(1, len(V0))]
    V1 = [sum(V1[:i]) / i for i in range(1, len(V1))]

    plt.plot(V0, label=f'flow0 :: {agent}')
    plt.plot(V1, label=f'flow1 :: {agent}')

plt.title(f'Packet Loss Rate (avg on {many} times)')
plt.grid()
plt.legend()
plt.xlabel('time(s)')
plt.ylabel('avg packet loss')
plt.show()
    

    