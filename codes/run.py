import os
import nstrace
import matplotlib.pyplot as plt
import random


filename = 'main.tcl'
agents = ['Agent/TCP', 'Agent/TCP/Newreno', 'Agent/TCP/Vegas']
agent_names = ['TCP', 'NewReno', 'Vegas']
ftr_name = 'test.tr'
fnm_name = 'test.nam'
many = 1

for agent, name in zip(agents, agent_names):

    t0s = []
    v0s = []
    t1s = []
    v1s = []
    for i in range(many):
        n23_d = str(int(random.uniform(5, 25))) + 'ms'
        n46_d = str(int(random.uniform(5, 25))) + 'ms'

        os.system(f'ns {filename} {agent} {n23_d} {n46_d} data/{name}{i}.tr data/{name}{i}.nam {1000}')