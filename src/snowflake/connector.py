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
    # 1. Create a Table
    create_sql = """
    CREATE OR REPLACE TABLE EXAMPLE_TABLE (
        ID integer,
        comments string
    )
    """
    cur.execute(create_sql)

    # 2. Insert Data
    insert_sql = """
    INSERT INTO EXAMPLE_TABLE (ID, comments)
    VALUES 
        (4, 'Sample comment 4'),
        (5, 'Sample comment 5'),
        (6, 'Sample comment 6')
    """
    cur.execute(insert_sql)

    # 3. Select Query
    select_sql = "SELECT * FROM EXAMPLE_TABLE"
    cur.execute(select_sql)
    for row in cur.fetchall():
        print(row)

    # 4. Update Data
    update_sql = """
    UPDATE EXAMPLE_TABLE
    SET comments = 'Updated comment'
    WHERE ID = 1
    """
    cur.execute(update_sql)

    # 5. Delete Data
    delete_sql = "DELETE FROM EXAMPLE_TABLE WHERE ID = 2"
    cur.execute(delete_sql)

    ''' NEEDS WORK
    # 6. Create a View
    create_view_sql = """
    CREATE OR REPLACE VIEW VIEW_EXAMPLE_TABLE AS
    SELECT *
    FROM EXAMPLE_TABLE
    WHERE comments LIKE '%Sample%'
    """
    cur.execute(create_view_sql)

    NEEDS WORK
    '''

    # 7. Aggregate Functions
    aggregate_sql = "SELECT COUNT(*) FROM EXAMPLE_TABLE"
    cur.execute(aggregate_sql)
    print(cur.fetchone())

    # 8. Join Operations
    # Create ANOTHER_TABLE
    create_another_table_sql = """
    CREATE OR REPLACE TABLE ANOTHER_TABLE (
        ID integer,
        detail string
    )
    """
    cur.execute(create_another_table_sql)

    # Assuming there's another table named ANOTHER_TABLE with columns ID and detail
    join_sql = """
    SELECT E.ID, E.comments, A.detail
    FROM EXAMPLE_TABLE E
    JOIN ANOTHER_TABLE A ON E.ID = A.ID
    """
    cur.execute(join_sql)
    for row in cur.fetchall():
        print(row)
finally:
    # Close the cursor and connection
    cur.close()
    conn.close()
