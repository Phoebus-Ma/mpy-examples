###
# MCU deep sleep.
#
# License - MIT.
###

# 深度睡眠，节能.
import time
import machine
from machine import deepsleep

# 防止无法刷机.
# 由于程序启动就执行deep sleep指令，刷其它程序时无法中断执行，而不得不重新刷机.
time.sleep(5)

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('RTC resume soc.')
else:
    print('Boot or reset.')

timeout = 10000
print('Enter deep sleep.')
machine.deepsleep(timeout)
