import pandas as pd
import glob
from sqlalchemy import create_engine
import os
import time
from datetime import datetime as dt


def get_files(pattern):
	return glob.glob(pattern)
	
def read_file(fname, txtfmt=False):
	if txtfmt:
		# HOBO TXT format
		df = pd.read_csv(fname, skiprows=2, header=None, sep='\s+', thousands=',', na_values='Logged')
		df['tstamp'] = [dt.strptime(row[1] + ' ' + row[2], '%d-%m-%y %H:%M:%S') for i, row in df.iterrows()]
		df.drop([0,1,2], axis=1, inplace=True)
		df.columns = ['temperature', 'light', 'tstamp']
	else:
		# HOBO CSV format
		df = pd.read_csv(fname, skiprows=2, header=None, parse_dates=[1], usecols=[1,2,3])
		#df.drop(0, axis=1, inplace=True)
		df.dropna(inplace=True)
		df.columns = ['tstamp', 'temperature', 'light']
		
	# add the current ID
	hobo_id = os.path.splitext(os.path.basename(fname))[0]
	df['hobo_id'] = hobo_id
	df.dropna(how='any', axis=0, inplace=True)
	
	return df


def load_to_table(data, engine, table):
	data.to_sql(table, engine, if_exists='append', index=False)

if __name__=='__main__':
	import sys
	if len(sys.argv) != 4:
		print("use like:   python imp.py PATTERN DB_URI TABLE")
		print("example :   python imp.py *.csv postgresql://uer:password@server:port/database raw_data")
		sys.exit()
		
	try:
		engine = create_engine(sys.argv[2])
		table = sys.argv[3]
	except:
		print('The DB_URI was not valid')
		sys.exit()
	
	print('-----------------------------------------------')
	files = get_files(sys.argv[1])
	print("Processing %d files..." % len(files))
	
	# get existing ids
	conn = engine.connect()
	res = conn.execute("select distinct hobo_id from %s where tstamp > '2019-06-06'" % table)
	existing_ids = [_[0] for _ in res.fetchall()]
	conn.close()
	
	for fname in files:
		hobo_id = int(os.path.splitext(os.path.basename(fname))[0])
		if hobo_id in existing_ids:
			print('%s aleady uploaded.' % fname)
		else:
			print('Uploading %s...' % fname)
			t1 = time.time()
			txtfmt = True if 'txt' in sys.argv[1] else False
			load_to_table(read_file(fname, txtfmt), engine, table)

			print('finished in %.1f seconds.' % (time.time() - t1))
		
	print('-----------------------------------------------')
	print('DONE!')
