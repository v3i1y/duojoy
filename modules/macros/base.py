import yaml
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'shared')))

import mapper

"""
Usage example:
    python3 modules/macro_runner/run_macro.py my_macro.yaml
"""

# 1. read macro file
macro_file_path = sys.argv[1]
with open(macro_file_path, 'r') as f:
    macro = yaml.load(f, Loader=yaml.FullLoader)

def run(events, repeats = 1):
    import pyvjoy
    j = pyvjoy.VJoyDevice(1)

    while True:
        for event in events:
            type, *params = event

            if type == mapper.VJOY_INPUT_TYPE_BUTTON:
                axis, duration, delay = params
                j.set_button(axis, True)
                time.sleep(duration)
                j.set_button(axis, False)

            if type == mapper.VJOY_INPUT_TYPE_POV:
                axis, duration, delay = params
                j.set_cont_pov(1, axis * 10000)
                time.sleep(duration)
                j.set_cont_pov(1, -1)

            time.sleep(delay)

        # negative repeat means infinite
        if repeats < 0:
            continue

        # repeat 0 means no repeats
        if repeats == 0:
            break

        repeats -= 1
