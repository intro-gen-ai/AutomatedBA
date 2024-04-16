Your task is to convert a text question to a SQL query that runs on Snowflake given a database schema. It is extremely important that you only return a correct and executable SQL query, with no added context.
`{preprompt}`: `{user_question}`

The query will run on a database with the following schema:
{table_metadata_string}

The following definitions may be of aid:
`{rag}`

Please return only the SQL query in your response, nothing else.
