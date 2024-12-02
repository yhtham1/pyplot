#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import datetime
import matplotlib.pyplot as plt
import japanize_matplotlib
import math


def main():

	# fig = plt.figure(figsize=(16,9))
	fig = plt.figure()
	ax1 = fig.add_subplot(1, 1, 1)
	# ax1.set_ylim(10, 40)

	x1 = []
	y1 = []
	for i in range(1000):
		x1.append(i)
		y1.append(5*math.sin(i/100)+5)

	ax1.plot(x1, y1, label='TypeA')

	ax1.legend()
	plt.show()


if __name__ == '__main__':
	main()

### EOF ###
