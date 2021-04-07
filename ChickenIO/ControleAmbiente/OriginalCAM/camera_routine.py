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
    now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S.jpg')
    arg = 'raspistill -n -q %s -o %s_%s' % (quality, base_name, now)
    Thread(target=os.system, args=([arg])).start()


def interval_capture(base_name='img', frames=5, t_beetw=10, quality=15):
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
	interval_capture(frames=2, quality=10)

