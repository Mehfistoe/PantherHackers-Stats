import pandas as pd
import numpy as np
import sqlite3

import itertools

def fuck_up_some_commas(string):
	string = string.strip()
	string = ''.join(ch for ch, _ in itertools.groupby(string))
	# if a comma is the first character, delete it
	if string.startswith(','):
		string = string[1:]
	# if a comma is the last character, delete it
	if string.endswith(','):
		string = string[:-1]
	string = string.strip()
	return string


conn = sqlite3.connect('phDB.db', timeout=10)
cur = conn.cursor()

df = pd.read_excel('Attendance_spreadsheets/demo_table.xlsx', header=0)

# replace all of the null values with string 'N/A'
df = df.replace(np.NaN, '')

"""
Take the hacker, hipster, hustler columns and combine them into one
Same with the reasons for joining PH
"""
hhh_df = pd.DataFrame({'hhh':df.iloc[:,6:9].apply(lambda x: ','.join(x), axis=1)})
reasons = pd.DataFrame({'reasons':df.iloc[:,10:17].apply(lambda x: ','.join(x), axis=1)})

# Drop the columns and replaces them with the new columns
df = df.drop(df.iloc[:,10:17],axis=1)
df = df.drop(df.iloc[:,6:9],axis=1)
df = pd.concat([df, reasons, hhh_df],axis=1)
df['Semester'] = 'Spring 2017'

for i, row in df.iterrows():
	fixed_cell_reasons = fuck_up_some_commas(row[7])
	fixed_cell_hhh = fuck_up_some_commas(row[8])
	df.set_value(i,'reasons',fixed_cell_reasons)
	df.set_value(i,'hhh',fixed_cell_hhh)
	
print(df)
cur.executemany("INSERT INTO Demographics VALUES (?,?,?,?,?,?,?,?,?,?)",
	(row for i, row in df.iterrows()))

conn.commit()
conn.close()
