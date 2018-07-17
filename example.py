#!/usr/bin/python
"""Example file for class DAC8552 in module dac8552:
Grading LED luminosity
Hardware: Waveshare High Precision AD/DA board interfaced to the Raspberry Pi 3
Narcisse Assogba, 2018-07-17
"""
import sys
from time import sleep

from dac8552 import DAC8552, DAC_A, DAC_B, MODE_POWER_DOWN_100K

# STEP 1: Initialise DAC object:
dac = DAC8552()

try:
    print("\033[2J\033[H")  # Clear screen
    print(__doc__)
    print("\nPress CTRL-C to exit.")

    dac.v_ref = 3.3
    step = int(3.3 * dac.digit_per_v / 10)

    direction = True
    i = 0
    while True:
        if direction:
            # STEP 2: Write to DAC:
            dac.write_dac(DAC_A, i * step)
            dac.write_dac(DAC_B, (10 - i) * step)
        else:
            dac.write_dac(DAC_A, (10 - i) * step)
            dac.write_dac(DAC_B, i * step)

        sleep(0.5)
        i += 1
        if i > 10:
            i = 0
            direction = not direction
except KeyboardInterrupt:
    print("\nUser exit.\n")
    # STEP 3: Put DAC to Power Down Mode:
    dac.power_down(DAC_A, MODE_POWER_DOWN_100K)
    dac.power_down(DAC_B, MODE_POWER_DOWN_100K)
    sys.exit(0)
