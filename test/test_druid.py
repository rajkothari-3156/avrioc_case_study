from pydruid.db import connect

# Establish a connection to your Druid broker
# Replace 'localhost' and '8082' with your Druid router/broker address and port
conn = connect(host='localhost', port=8082, path='/druid/v2/sql/', scheme='http')

# Create a cursor object
cursor = conn.cursor()

# Execute a SQL query
cursor.execute("SELECT __time, channel, count(*) FROM wikipedia WHERE __time >= '2015-09-12T00:00:00Z' AND __time < '2015-09-13T00:00:00Z' GROUP BY __time, channel ORDER BY __time LIMIT 5")

# Fetch the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the connection
cursor.close()
conn.close()