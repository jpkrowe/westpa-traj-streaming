from westpa.tools.trajectory_streaming import TrajectoryStreamer
import numpy as np
from MDAnalysis.analysis.distances import self_distance_array


numthreads = 1

stream = TrajectoryStreamer(
    "gromacs",
    "bstate.gro",
    f"gmx_imd mdrun -s seg.tpr -o seg.trr -c seg.gro -e seg.edr -cpo seg.cpt -g seg.log -nt {numthreads} -imdwait -imdport 0"
)
u = stream.start_sim_and_get_universe()

ag = u.select_atoms("not water")

dist = []
for ts in u.trajectory:
    dist.append(self_distance_array(ag)[0])
# print(np.array(dist).T)
np.savetxt("dist.dat", np.array(dist))