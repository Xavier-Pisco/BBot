import os
import subprocess

newpid = os.fork()
try:
	if newpid == 0:
		subprocess.call(["python3", "bot.py"])
	else:
		subprocess.call(["python3", "bot2.py"])
except KeyboardInterrupt:
    os.kill(newpid, signal.SIGTERM)
    print("Bye!")