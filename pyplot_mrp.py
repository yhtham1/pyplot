#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import matplotlib.pyplot as plt
import japanize_matplotlib
import matplotlib.ticker as ptick
from cycler import cycler


def monochrome_style_generator():
	linestyle = ['-', '--', '-.', ':']
	markerstyle = ['h', '2', 'v', '^', 's', '<', '>', '1', '3', '4', '8', 'p', '*', 'H', '+', ',', '.', 'x', 'o', 'D',
				   'd', '|', '_']
	line_idx = 0
	marker_idx = 0
	while True:
		yield 'k' + linestyle[line_idx] + markerstyle[marker_idx]
		line_idx = (line_idx + 1) % len(linestyle)
		marker_idx = (marker_idx + 1) % len(markerstyle)


# Create cycler object. Use any styling from above you please
"""
':' 点線

"""
monochrome = (cycler('color', ['k']) * cycler('linestyle', ['-', '--', '-.', ':']) * cycler('marker', [',', '.', '^']))


# Print examples of output from cycler object.
# A cycler object, when called, returns a `iter.cycle` object that iterates over items indefinitely
def print_cycle():
	print("number of items in monochrome:", len(monochrome))
	for i, item in zip(range(15), monochrome()):
		print(i, item)


def get_tail(txt1, word):
	ans = txt1[txt1.find(word) + len(word):]
	return ans


def get_serialnumber(txt_idn):
	"""
	メーカー,型式,シリアル,ファームバージョン
	:param txt_idn:
	:return:
	"""
	ans = ''
	k = txt_idn.split(',')
	ans = k[2].strip()
	return ans


def is_float(s):
	try:
		float(s)
	except ValueError:
		return False
	return True


def extract_file(filename, colx, coly):
	sn_mrp = ''
	sn_mv2 = ''
	date1 = ''
	lbl = os.path.basename(filename)
	ansx = []
	ansy = []
	try:
		with open(filename, 'rt') as f:  # 全体をよみこむ。
			txt1 = f.readlines()
	except:
		with open(filename, 'rt', encoding='utf-8') as f:  # 全体をよみこむ。
			txt1 = f.readlines()
	for l1 in txt1:
		l2 = l1.strip()
		if 0 < l2.find('LOG START'):
			ansx = []
			ansy = []
			date1 = ''
		if 0 < l2.find('mv2serial'):
			sn_mv2 = 'MV2:' + get_tail(l2, 'mv2serialnumber:')
		if 0 < l1.find('*IDN?:'):
			sn_mrp = 'MRP:' + get_serialnumber(get_tail(l1, '*IDN?:'))
		k = l2.split('\t')
		if 0 <= l1.find('#'):
			print(l2)
			continue
		if len(k) < colx:
			continue
		if len(k) < coly:
			continue
		if False == is_float(k[colx]):
			continue
		# print(k[colx],k[coly])
		ansx.append(float(k[colx]))
		ansy.append(float(k[coly]))
		date1 = k[0].strip()
	if '' != sn_mrp:
		lbl = sn_mrp
	if '' != sn_mv2:
		lbl += '-' + sn_mv2
	if '' != date1:
		lbl += '-' + date1
	return ansx, ansy, lbl


"""
ファイル名から推測する場合
含まれるワード	'ノイズ' '_freq'
TIMESTAMP	TXFREQ	MV2_TEMP	SIGNAL	NOISE

含まれるワード	'周波数特性' 受信機の周波数特性
TIMESTAMP	FREQ	プローブ温度	シグナル	ノイズ	

含まれるワード	'_MV2'	磁場ロック値
TIMESTAMP	VOLT	MV2_d	NMR_FREQ	MV2_FREQ	MV2_FREQ_RAW	MV2_TEMP	SIGNAL	NOISE

"""


def main():
	argn = len(sys.argv)
	# print(sys.argv)
	fn1 = []
	for fn2 in sys.argv[1:]:
		fn = fn2.strip()
		if 0 < fn.find('SN'):
			continue
		if 0 < fn.find('SIGNAL'):
			continue
		fn1.append(fn)

	if 0 == len(fn1):
		print('file not found')
		return
		fn1.append('20210305_1435_log_MV2.txt')
		fn1.append('20210305_1357_log_MV2.txt')
	# fn1.append('ノイズ特性_C21010037_20210120_1402.txt')
	# fn1.append('ノイズ特性_C21030011_20210304_1703.txt')
	# fn1.append('ノイズ特性_C21030011_20210305_1254.txt')

	# fig = plt.figure(figsize=(16,9))
	fig = plt.figure()
	ax1 = fig.add_subplot(1, 1, 1)
	ax1.set_prop_cycle(monochrome)
	ax1.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
	ax1.set_ylim(-40, 10)

	for filename in fn1:
		if 0 < filename.find('MV2'):
			x1, y1, lbl1 = extract_file(filename, 3, 7)
		else:
			x1, y1, lbl1 = extract_file(filename, 1, 3)
		ax1.set_xlabel('周波数(Hz)')
		ax1.set_ylabel('signal(dB)')
		# plt.plot(x1, y1, label=lbl1)
		ax1.plot(x1, y1, label=lbl1)

	# ax1.xaxis.offsetText.set_fontsize(14)
	ax1.xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
	plt.title('SIGNAL')
	ax1.legend()
	plt.show()
	# print_cycle()
	pass


if __name__ == '__main__':
	main()

### EOF ###
