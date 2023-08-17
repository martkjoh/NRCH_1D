# Timesteps, gridpoints, length
const M = 10_000_000
const N = 500
const L = N/5.
const c = .01 # dt/dx^4 = c
# P rint progress bar
pr = true
# Folder for data
write_folder = "data/long_cold/"
rm(write_folder, recursive=true, force=true)
mkdir(write_folder[1:end-1])

include("numerics.jl")


using Base.Threads
u = 10.
D = 1e-12

u = 10.
D = 1e-5
bφ = -.2
α = 2.
param = (u, α, D, bφ)

circs = [false, false, false, true]

@time @threads for circ in circs
    @time run_euler(param; circ=circ)
end
