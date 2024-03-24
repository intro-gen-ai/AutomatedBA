import snowflake.connector

# Snowflake connection parameters
conn_params = {
    'user': 'TASTY_USER',
    'password': 'securePassword123!',
    'account': 'xuogpub-eq51122',
    'warehouse': 'TASTY_BITES_WH',
    'database': 'TASTY_BITES_SAMPLE_DATA',
    'schema': 'PUBLIC',
}

# Create a connection to Snowflake
conn = snowflake.connector.connect(**conn_params)

# Create a cursor object
cur = conn.cursor()


try:
    # Execute a query
    sql = ("CREATE OR REPLACE TABLE EXAMPLE_TABLE"
           " (ID integer, comments string)")
    cur.execute(sql)
    #cur.execute("SELECT * FROM TASTY_BYTES_SAMPLE_DATA LIMIT 10")

    # Fetch the result set from the cursor and print
    #for row in cur:
     #   print(row)
finally:
    # Close the cursor and connection
    cur.close()
    conn.close()
