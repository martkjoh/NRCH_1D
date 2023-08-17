from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
from numpy import pi, sqrt


from loadfiles import *

plt.rc("font", family="serif", size=16)
plt.rc("mathtext", fontset="cm")
plt.rc("lines", lw=2)



def make_anim(folder, filenames):
    filenames = [f[:-4] for f in filenames]

    phitparams =  [load_file(folder, filename) for filename in filenames]
    param = phitparams[0][1]
    u, a, b, phibar, N, L, T, dt = param 
    phits = [phit for (phit, param) in phitparams]

    dx = L / N
    x = np.linspace(0, L, N)

    fig = plt.figure(layout="constrained", figsize=(12, 18))
    fig.suptitle(", ".join(filename_from_param(param).split('_')))

    gs = GridSpec(6, 2, figure=fig)
    ax = []

    ind = [(0, 0), (1, 0), (0, 1), (1, 1)]
    for i,j in ind:
        i = i * 3
        axa = fig.add_subplot(gs[0+i:1+i, j])
        axb = fig.add_subplot(gs[1+i:3+i, j])
        ax.append([axa, axb])

    
    ls = []
    ms = []
    t = np.linspace(0, 2*pi)
    prange = 1.2
    frames = len(phits[0])
    n = 100

    for i, axi in enumerate(ax):
        axa, axb = axi

        l1, = axa.plot([], [], 'r-', label='$\\varphi_1$')
        l2, = axa.plot([], [], 'k-', label='$\\varphi_2$')
        axa.plot([0, L], [phibar, phibar], 'r--')
        axa.plot([0, L], [0, 0], 'k--')
        axa.set_xlim(0, L) 
        axa.set_ylim(-1.2, 1.2)
        axa.legend(loc=1)

        ls.append([l1, l2])

        m, = axb.plot([], [], 'r--.')
        axb.plot(0, phibar, 'ro')
        axb.plot(np.cos(t), np.sin(t), 'k--') 
        axb.set_xlim(-prange, prange)
        axb.set_ylim(-prange, prange)

        ms.append(m)

    def animate(k):
        k = k*n

        for i, phit in enumerate(phits):
            l1, l2 = ls[i]
            m = ms[i]
            p = phit[k]
            l1.set_data(x, p[:, 0])
            l2.set_data(x, p[:, 1])
            m.set_data([*p[:, 1], p[0, 1]], [*p[:, 0], p[0, 0]])

    anim = animation.FuncAnimation(fig, animate, cache_frame_data=False, blit=True,  interval=1, frames=frames//n, repeat=False)
    plt.show()
    # anim.save(folder_vid+filename+".mp4", fps=30)

name = "traveling"
folder = "data/" + name + "/"
folder_vid = "vid/" + name + "/"

import os, shutil
from multiprocessing import Pool, current_process
if os.path.isdir(folder_vid):
    shutil.rmtree(folder_vid)
os.mkdir(folder_vid)

fnames = get_all_filenames_in_folder(folder)

import time
startTime = time.time()


make_anim(folder, fnames)


executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))


