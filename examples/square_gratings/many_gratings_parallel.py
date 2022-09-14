import meep as mp
# import meep_retrieval as mr
import numpy as np
import matplotlib.pyplot as plt
from meep.materials import Au, Ag

import sys
sys.path.append('../metamaterials')
from metamaterials import meep_retrieval as mr

## Simulation definition
# Frequency range
lambda_min = 1
lambda_max = 4
nfreqs = 100
pol = mp.Ex # Polarization
t = 0.020 # Thickness of metal layer
dir = 'results/test3' # Directory to save results

N = 2
n = mp.divide_parallel_processes(N)

a = np.linspace(2.75, 5, N)
a = a[n] # Choose one of the indicies for each process
d = 0.8*a

index = 3.5

sim = mr.Simulation(resolution=60, cell=a, fmin=1/lambda_max, fmax=1/lambda_min, nfreqs=nfreqs, pol=pol, directory=dir)

material = mp.Medium(index=index)
geometry = [mp.Block(size=mp.Vector3(d, d, t), center=mp.Vector3(0, 0, -t/2), material=material)]
sim.set_geometry(geometry, material)

sim.run()

[S11, S21] = sim.get_s_params()

mp.all_wait()

S11 = mp.merge_subgroup_data(S11)
S21 = mp.merge_subgroup_data(S21)

for i in range(N):
    s11 = [a[i] for a in S11]
    s21 = [a[i] for a in S21]
    plt.figure()
    plt.plot(sim.get_freqs(), np.abs(s11)**2)
    plt.plot(sim.get_freqs(), np.abs(s21)**2)
    print('saving figure ', i)
    a = np.linspace(2.75, 5, N)
    plt.savefig('size_%d.png' % a[i])

