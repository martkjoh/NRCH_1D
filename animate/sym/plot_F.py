import numpy as np
import matplotlib.pyplot as plt

import os, sys
sys.path.insert(0, os.path.abspath("./"))
from loadfiles import *


folder = "data/test/"
folder_vid = "numerics/vid/"


fnames = get_all_filenames_in_folder(folder)
filename = fnames[0]
filename = filename[:-4]

param = param_from_filename(filename)


phit, param = load_file(folder, filename)

skip = 10
M0 = len(phit)
phit = phit[skip:]
u, a, b, phibar, N, L, T, dt = param
M = len(phit)
T = M * dt
t = np.linspace((M0 - M)*dt, T + dt, M)
L = 10.
dx = L / N
D2 = lambda J : ( np.roll(J, 1, axis=1) + np.roll(J, -1, axis=1) - 2 * J ) / dx**2


aeps = a * np.array([[0, 1], [-1, 0]])

p2 =  np.sum(phit**2, axis=2)
dF = u * (-1 + p2 )[:, :,  None] * phit - D2(phit)
mut = np.einsum("ij,tnj->tni", aeps, phit)
mu = (dF + mut)[:-1] 
dtphi = D2(mu)
fdot = np.sum(dtphi * dF[:-1], axis=2)
Fdot = np.sum(fdot, axis=1) * dx * 1000

f1 = u * (- p2 / 2 + p2**2 / 4 ) - np.sum(phit * D2(phit), axis=2 )/ 2
F1 = np.sum(f1, axis=1) * dx

F2 = np.concatenate([[F1[0],], Fdot*dt])
F2 = np.cumsum(F2)


fig, ax = plt.subplots()

 
ax.plot([0, T], [0, 0], "k--")
dFdt = np.diff(F1) / np.diff(t)

ax.plot((t[:-1] + t[1:])/2, dFdt, ls="--", color='red')
ax.plot(t[:-1], Fdot, ls="--", alpha=1, color='blue')


ax2 = plt.twinx(ax)
ax2.plot(t, F1, label="F actual", color='r')
ax2.plot(t, F2, label="F integrated", color='blue')
ax2.plot([0, T], [F1[-1], F1[-1]], 'k--')
# ax.set_xlim(.1, .16)


plt.legend()
plt.show()