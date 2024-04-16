### Task
Your task is to convert a text question to a SQL query that runs on Snowflake, given the database schema: {table_metadata_string}. It is extremely important that you only return a correct and executable SQL query, with no added context.
`{instruction_set}`

### Input:

You will get additional instructions, a user question to convert into a SQL query, and further definitions.

### Answer
Given the database schema, here is the SQL query that answers [QUESTION]`{user_question}`[/QUESTION]
[SQL]
