from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
from numpy import pi, sqrt

import os, sys
sys.path.insert(0, os.path.abspath("./"))
from loadfiles import *

plt.rc("font", family="serif", size=16)
plt.rc("mathtext", fontset="cm")
plt.rc("lines", lw=2)



def plot_error(ax, phit, param):
    u, a, b, phibar1, phibar2, N, L, T, dt = param
    dx = L / N
    pt = np.einsum('txi->ti', phit) * dx / L
    dpt = (pt[1:] - pt[:-1])/dt
    frames = len(phit)
    t = np.linspace(0, frames*dt, frames-1)
    ax.plot(t, dpt[:,0], label="$\\frac{\\mathrm{d} \\bar \\varphi_1}{\\mathrm{d} t}$")
    ax.plot(t, dpt[:,1], label="$\\frac{\\mathrm{d} \\bar \\varphi_2}{\\mathrm{d} t}$")

    ax2 = ax.twinx()
    t = np.linspace(0, frames*dt, frames)
    ax2.plot(t, pt[:, 0]-pt[0,0], 'k--', label="$\\varphi_1(t) - \\varphi_1(0)$")
    ax2.plot(t, pt[:, 1]-pt[0,1], 'r--', label="$\\varphi_2(t) - \\varphi_2(0)$")

    ax.set_ylabel("$\\dot{\\bar\\varphi}$")
    ax.set_xlabel("$t$")
    ax2.set_ylabel("$\\Delta\\bar\\varphi$")

    legend_1 = ax.legend(loc=3)
    legend_1.remove()
    ax2.add_artist(legend_1)
    ax2.legend(loc=4)

def make_anim(folder, filename):
    filename = filename[:-4]

    phit, param = load_file(folder, filename)
    u, a, b, phibar1, phibar2, N, L, T, dt = param
    dx = L / N
    x = np.linspace(0, L, N)

    fig = plt.figure(layout="constrained", figsize=(8, 10), dpi=100)
    gs = GridSpec(4, 1, figure=fig)
    ax1 = fig.add_subplot(gs[0]) 
    ax2 = fig.add_subplot(gs[1:])

    ax = [ax1, ax2]

    l1, = ax[0].plot([], [], 'r-', label='$\\varphi_1$')
    l2, = ax[0].plot([], [], 'k-', label='$\\varphi_2$')
    ax[0].plot([0, L], [phibar1, phibar1], 'r--')
    ax[0].plot([0, L], [phibar2, phibar2], 'k--')

    ax[0].set_xlim(0, L) 
    ax[0].set_ylim(-1.2, 1.2)
    ax[0].legend(loc=1)
    l5 = ax[0].text(L/10, 1, 'progress:')

    t = np.linspace(0, 2*pi)
    prange = 1.2
    m1, = ax[1].plot([], [], 'r--.')
    ax[1].plot(phibar2, phibar1, 'ro')
    ps = 1/sqrt(2)
    ax[1].plot([ps, ps, -ps, -ps, ps], [ps, -ps, -ps, ps, ps], 'k--') 
    ax[1].set_xlim(-prange, prange)
    ax[1].set_ylim(-prange, prange)
    ax[1].set_xlabel("$\\varphi_2$")
    ax[1].set_ylabel("$\\varphi_1$")

    frames = len(phit)

    n = 10
    def animate(m):
        m = m*n
        n2 = frames//10
        txt = 'progress:' + (m+1)//n2*'|'
        l5.set_text(txt)

        p = phit[m]
        l1.set_data(x, p[:, 0])
        l2.set_data(x, p[:, 1])

        m1.set_data([*p[:, 1], p[0, 1]], [*p[:, 0], p[0, 0]])

        n3 = frames//100
        if m//n3 - (m-n)//n3 == 1:
            txt = str((m+1)//n3) + "%"
            print(current_process().name, '\t', txt)

    anim = animation.FuncAnimation(fig, animate, cache_frame_data=False, interval=1, frames=frames//n, repeat=True)
    # plt.show()
    anim.save(folder_vid+filename+".mp4", fps=10)

names = [
    # "short",
    # "long",
    # "long_cold",
    # "long_hot", 
    "test2",
    # "test3",
    # "chaotic"
    # "additional"
    ]

for name in names:
    folder = "data/assym/" + name + "/"
    folder_vid = "vid/assym/" + name + "/"

    import os, shutil
    from multiprocessing import Pool, current_process
    if os.path.isdir(folder_vid):
        shutil.rmtree(folder_vid)
    os.mkdir(folder_vid)

    fnames = get_all_filenames_in_folder(folder)


    import time
    startTime = time.time()

    [make_anim(folder, fname) for fname in fnames[:]]

    # folder_fname = [(folder, name) for name in fnames]
    # with Pool(10) as pool:
    #     pool.starmap(make_anim, folder_fname)

    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(executionTime))
