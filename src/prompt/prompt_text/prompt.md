### Task
Your task is to convert a text question to a SQL query that runs on Snowflake given a database schema. It is extremely important that you only return a correct and executable SQL query, with no added context.
`{preprompt}`: [QUESTION]`{user_question}`[/QUESTION]
The following definitions may be of aid:
`{rag}`

### Database Schema
The query will run on a database with the following schema:
{table_metadata_string}

### Answer
Given the database schema, here is the SQL query that answers [QUESTION]`{user_question}`[/QUESTION]
[SQL]
