


import os


duration = 1  # second
freq = int(raw_input("frequency:"))  # Hz
while True:
	os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
  # Hz
