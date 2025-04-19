###
# EPS controller state.
#
# License - MIT.
###

import machine
import esp
import esp32


size = esp.flash_size()
print(size)

freq1 = machine.freq()
# esp32c6: 20MHz, 40MHz, 80MHz, 160MHz.
machine.freq(20000000)
freq2 = machine.freq()
machine.freq(160000000)
freq3 = machine.freq()
print(freq1, freq2, freq3)
