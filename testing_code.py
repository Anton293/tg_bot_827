#import wifi

import os
import time

while True:
    _temp = os.popen('vcgencmd measure_temp').readline()
    temp = float(_temp.replace("temp=", "").replace("C", ""))
    print(temp)
    time.sleep(60)

