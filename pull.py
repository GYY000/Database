import os
import time
while True:
    result = os.system("git pull")
    if result == 0:
        quit()
    time.sleep(1)
    print(result)