### Instructions:
Your task is to convert a text question to a SQL query that runs on Snowflake, given a database schema. Return the SQL as a markdown string, nothing else.

### Input:
`{preprompt}`: `{user_question}`.
`{instructions}`
This query will run on a database whose schema is represented in this string:
{table_metadata_string}
### Response:
Given the database schema, here is the SQL query that answers `{user_question}`:
```sql
