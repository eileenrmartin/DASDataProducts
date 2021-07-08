import sqlite3
import sys
# creating file path

dbfile = '/content/drive/MyDrive/20201202_Kafadar/UTC-YMD20201202-HMS174339.516/metadata/Kafadar_Coupling_deformation_UTC-YMD20201202-HMS175221.177_seq_00000000004.hdf5.db'
#dbfile = sys.argv[1]

# Create a SQL connection to our SQLite database
con = sqlite3.connect(dbfile)

# creating cursor
cur = con.cursor()
# reading all table names
table_list = [a for a in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]
# here is you table list
print(table_list)
for row in cur.execute("SELECT * FROM frames"):
    print(row)
# Be sure to close the connection
con.close()