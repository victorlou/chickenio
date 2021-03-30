# -*- coding: utf-8 -*-
"""
Created on March 29 2021

@author: Victor Feitosa Lourenco
"""

""" -------- LIBRARIES -------- """
import os
import time
from threading import Thread
from datetime import datetime
""" --------------------------- """


def single_frame(base_name='img', quality=50):
"""
Description: takes a single camera shot using the Raspberry Pi default
             camera interface with a simple system comand line. This
             action is threadded, since it takes around six (6) seconds
             to be completed and can congest code flow.

Parameters:
- base_name (string): string with which the image will be saved,
                      concatenated with the current datetime.
- quality (int): number between 0 and 100 to dictate image quality.

Returns: None
"""
	now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
	arg = f'raspistill -n -q {quality} -o {base_name}_{now}'
	Thread(target=os.system, args=([arg])).start()


def interval_capture(base_name='img', frames=3, t_beetw=10, quality=50):
"""
Description: uses single_frame to take multiple shots with a defined
             time interval between them.

Parameters:
- base_name (string): see single_frame.
- frames (int): number of frames (greater than zero) which will be taken
                in total.
- t_beetw (int): number of seconds between each frame.
- quality (int): see single_frame.


Returns: None
"""
	# camera usually takes 6 seconds to adjust lighting, etc
	if t_beetw <= 6:
		print('ERROR: time between frames is too short!')
		return
	
	frame_count = 0
	while frame_count < frames:
		single_frame(base_name=base_name, quality=quality)
		time.sleep(t_beetw)
		frame_count += 1


if __name__ == "__main__":
	interval_capture(frames=5, quality=15)
	
