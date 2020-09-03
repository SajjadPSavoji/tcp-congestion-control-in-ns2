import os

filename = 'reno_vs_vegas.tcl'
for i in range(3):
    os.system(f'ns {filename} {i}')