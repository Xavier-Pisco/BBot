import os
import subprocess
import keep_alive

newpid = os.fork()
try:
	if newpid == 0:
		subprocess.call(["python3", "bot.py"])
	else:
		keep_alive.keep_alive()
except KeyboardInterrupt:
    os.kill(newpid, signal.SIGTERM)
    print("Bye!")
except Exception as e:
	print(e)