System: Your task is to convert a text question to a SQL query that runs on Snowflake given a database schema. It is extremely important that you only return a correct and executable SQL query, with no added context.
User: `{preprompt}`: `{user_question}`. 
This query will run on a Snowflake database whose schema is represented in this string:
{table_metadata_string} 
The following definitions may be of aid:
`{rag}`
