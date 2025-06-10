import MDAnalysis as mda
from MDAnalysis.analysis.distances import self_distance_array
import numpy as np
from imdclient.IMD import IMDReader
import socket 
import time
import sys

port_open = False
timeout=0.2
port=int(sys.argv[1])
host="localhost"
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
while not port_open:
#     sock.settimeout(timeout)
    try:
        sock.connect((host, port))
    except ConnectionRefusedError:
        time.sleep(timeout)
    else:
        print(f"Port {port} on {host} is now open!")
        port_open = True

# sock.close()

u = mda.Universe('bstate.gro', f"imd://localhost:{port}")
ag = u.select_atoms('not water')

dist = []
for ts in u.trajectory:
    dist.append(self_distance_array(ag)[0])
# print(np.array(dist).T)
np.savetxt("dist.dat", np.array(dist))
