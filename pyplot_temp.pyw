#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import japanize_matplotlib
import matplotlib.ticker as ptick
from cycler import cycler


def monochrome_style_generator():
	linestyle = ['-', '--', '-.', ':']
	markerstyle = ['h', '2', 'v', '^', 's', '<', '>', '1', '3', '4', '8', 'p', '*', 'H', '+', ',', '.', 'x', 'o', 'D',
				   'd',
				   '|', '_']
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

def is_datetime(ts:str):
	dt = datetime.datetime.now()
	fmt1 = '%Y/%m/%d %H:%M:%S'
	dt1 = datetime.datetime.strptime(ts, fmt1)
	return dt



def extract_one_file(filename, colx, coly, sn_mode = False):
	# print('extract_file({} x={} y={})'.format(filename, colx, coly))
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
		if 0 < l2.find('mv2serial'):
			sn_mv2 = 'MV2:' + get_tail(l2, 'mv2serialnumber:')
		k = re.split(r'[,]', l2)
		if len(k) < colx:
			continue
		if len(k) < coly:
			continue
		try:
			fmt1 = '%Y/%m/%d %H:%M:%S'
			dt1 = datetime.datetime.strptime(k[colx], fmt1)
		except:
			continue
		# is_datetime(k[colx])
		# if False == is_date(k[colx]):
		# 	continue
		# print('date:{} temp:{}'.format(dt1,k[coly]))
		ansx.append(dt1)
		# ansx.append(k[colx])
		ansy.append(float(k[coly]))
		date1 = k[0].strip()
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


def get_filedatetime(path_p):
	update_time = datetime.datetime.fromtimestamp(path_p.stat().st_mtime)  # 更新時刻
	ans = update_time.strftime('%Y-%m-%d %H:%M:%S')
	# print('stat:{} '.format( ans))
	return ans


def usage():
	cmd = sys.argv[0]
	p = Path(cmd)
	print('{} グラフを表示する。'.format(p.name))
	print('Usage:')
	print('\t{} [--x <ｘ軸のカラム(0..)>] [--y <y軸のカラム(0..)>] テキストファイル'.format(p.name))


def main():
	COLOR_MODE = False
	SN_MODE = False
	TITLE = 'SIGNAL'
	fn1 = []
	col_x = 1
	col_y = 3
	i = 1
	while i in range(len(sys.argv)):  # fn2 in sys.argv[1:]:
		fn2 = sys.argv[i]
		fn = fn2.strip()
		if 0 == fn.find('color'):
			COLOR_MODE = True
			i += 1
			continue
		if 0 == fn.find('SN'):
			SN_MODE = True
			i += 1
			continue
		if 0 == fn.find('SIGNAL'):
			i += 1
			continue
		if 0 == fn.find('--x'):
			col_x = int(sys.argv[i + 1])
			i += 2
			continue
		if 0 == fn.find('--y'):
			col_y = int(sys.argv[i + 1])
			i += 2
			continue
		fn1.append(fn)
		i += 1

	fn1.append('d:/tmp3/local7.log')

	if 0 == len(fn1):
		usage()
		print('file not found')
		return

	path_p = Path(sys.argv[0])
	fig,ax = plt.subplots()
	ax.grid()
	fig.autofmt_xdate()
	ax.set_xlabel('date')
	ax.set_ylabel('温度(℃)')

	for filename in fn1:
		TITLE = '室温'
		col_x = 1 # NMR FREQ
		col_y = 2 # SIGNAL
		x1, y1, lbl1 = extract_one_file(filename, col_x, col_y, SN_MODE)
		ax.plot(x1, y1, label=lbl1)

	# ax1.xaxis.offsetText.set_fontsize(14)
	# ax1.xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
	plt.title(TITLE)
	# ax1.legend()
	plt.show()
	# print_cycle()
	pass



if __name__ == '__main__':
	main()

### EOF ###
