# Connect to mysql database
import mysql.connector

config = {
	'user': 'root',
	'password': '',
	'host': 'localhost',
	'database': 'python_test',
	'port': 3306
}

try:
	conn = mysql.connector.connect(**config)
except:
	print("Unable to connect")


sql = "INSERT INTO student(name,roll_number,fees) VALUES(%s, %s, %s)"
myc = conn.cursor()
params = ('Jai',190,19000.00)

try:
	myc.execute(sql, params)
	conn.commit()   # Committing the change
	print(myc.rowcount, "Row Inserted")
	# print("Total row inserted: ", myc.rowcount)
	# print("Last row id: ",myc.lastrowid)
except:
	conn.rollback()
	print("Unable to print data")

myc.close()
conn.close()


