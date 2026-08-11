import subprocess, time, sys, os
print("Starting 5 Mesh Nodes...")
procs = []
for i in range(1,6):
    port = 9000+i
    p = subprocess.Popen([sys.executable, "node.py", str(port)])
    procs.append(p)
    time.sleep(0.5)
print("5 Nodes Running. Starting Dashboard...")
time.sleep(1)
subprocess.run([sys.executable, "app.py"])