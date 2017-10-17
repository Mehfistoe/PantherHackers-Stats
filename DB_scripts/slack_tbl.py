
"""NOTES: triple double quotes are for multi-line comments
# for single line comments
csv: comma separated file
"""

"""Populating the Slack table in the PHDB"""
"""First we import the libraries (or modules as they're called in Python
for this task"""

#sqlite3 is for interacting with the sqlite DB we have
import sqlite3

#pandas is for making the csv file easier to manipulate
import pandas as pd

# Create a Connection object that connects to the DB
conn = sqlite3.connect('phDB.db')
# Create the Cursor object to allow us to execute SQL commands
cur = conn.cursor()

"""Then, we put the csv file into a pandas dataframe. 
Think of dataframes as spreadsheets you can edit programmatically. I put the
csv file into a dataframe so that the data is easier to retrieve (syntactically
anyway (I'm pretty sure I spelled that wrong))."""

# Puts csv file into a dataframe
# header=0 designates the first row as the column titles
df = pd.read_csv('slack_data.csv', header=0)

"""Now we go through each row of the df and put in the necessary values into
the sqlite DB"""
for i, row in df.iterrows():
	# Using the Cursor object for SQL commands
	cur.execute("INSERT INTO Slack VALUES (?,?,?,?,?,?,?)",
			(row[0],row[1],row[4],row[5],row[8],row[9],row[11]))

# commit the changes
conn.commit()
# Close the DB (SUPER IMPORTANT FOR SECURITY REASONS)
conn.close()

