import subprocess
import re
import MDAnalysis as mda
from MDAnalysis.analysis.distances import self_distance_array
import numpy as np
from imdclient.IMD import IMDReader
import socket 
import time

proc =subprocess.Popen(["gmx_imd", "mdrun", "-s", "seg.tpr", 
                        "-o", "seg.trr", "-c", "seg.gro", "-e", "seg.edr", 
                        "-cpo", "seg.cpt", "-g", "seg.log", 
                        "-nt", "1", "-imdwait", "-imdport", "0"]
                        ,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
assigned_port = None

for line in proc.stdout:
    print(line, end="") 
    m = re.search(r'IMD connection on port (\d+)', line)
    if m:
        assigned_port = int(m.group(1))
        break
print(f"Assigned IMD port: {assigned_port}")

port=assigned_port
port_open = False
timeout=0.2
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