### Instructions:

Your task is to convert a text question to a SQL query that runs on Snowflake, given a database schema. Return the SQL as a markdown string, nothing else.

### Operational Definitions

The following definitions are important to understand in context:
{rag_context}

### Input:

`{preprompt}`: `{user_question}`.
`{instructions}`
This query will run on a database whose schema is represented in this string:
{table_metadata_string}

### Response:

Given the database schema and context, here is the SQL query that answers `{user_question}`:

```sql

```
