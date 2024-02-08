# AutomatedBA

Proposal:
Project Pitch, Due January 30: The project proposal should be at most two slides, and should describe:
• What is the problem you will be attempting to solve, or the question you will be trying to answer?

Develop a natural language interface for SQL databases, allowing users to query databases using plain language without needing SQL or graphical library expertise. The goal is to integrate a GPT model with a database (like Snowflake) and enhance this integration with additional technologies to improve query generation and processing.

• Why is this an interesting project for your peers to consider?

Almost every business in the US with a SQL database would want this to exist and no one has fully solved it yet and the window is closing. It would be a fantastic project both for a portfolio and to possibly sell if we do well.

• What approaches are you considering and which ones will you experiment with?

	We have four main ways of ripping this problem apart:
SQL Compiler: Use Snowflake's decompiler to build an evaluator that optimizes based on table sizes.
Lang-Chain Pre-prompting: Use a context generation method to produce more accurate prompts.
Semantics Layer: Enhance “understanding” with contextual analysis, entity recognition and categorization, and synonym handling.
Query Splitting: Break down complex queries into simple ones.

• How will you evaluate your results? What are you looking for (qualitatively) that you would call a success?

Success measured using a test suite of SQL queries on a specific database. The test suite will have to be hand made and a set of different common algorithms with the correct solution for the test data.
The system has two primary metrics: runtime (efficiency) and accuracy. 
Accuracy is most important, with efficiency serving as a mere differentiator between equally accurate solutions.

Group:
Gabe Denton,
Luke Gries,
Ananth Josyula,
Mayaank Pillai

Our roles are not yet decided.

Objective:


To successfully integrate GPT-4 with modules to increase its accuracy and performance in SQL queries. These modules will be 1) an agent 2) a semantics layer 3) LangChain to pre-read the prompt and create a set of information to attach to the query to inform GPT-4 so that the exact/proper algorithm is performed 3) an estimator of SQL query time to choose the most efficient query 4) a script to perform multiple GPT-4 calls and collect multiple queries to evaluate before choosing the best. These modules will all hopefully increase its performance and we will evaluate this with an accuracy biased testing set we will manually create.
