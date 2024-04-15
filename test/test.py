import pandas as pd
import os


path = os.path.dirname(os.path.realpath(__file__))

df = pd.read_csv(os.path.join(path, "questions_gen_snowflake.csv"))
results = []
for index, row in df.iterrows():
    print("H")
    database = row["db_name"]
    question = row["question"]

    gt_query = row["query"]

    # TODO: bunch of stuff
    """ 1. run model on user question and database schema. we can set the parameters we're testing
        2. get snowflake output from both gt_query and model output
        3. get gt and model snowflake results as a dataframe. Search : cursor.fetch_pandas_all()
        
        not sure how snowflake handles errors, may need try-catch. return empty dataframe if query results in an error
    """

    gt_result = pd.DataFrame(df)  # DUMMY RESULT, CHANGE
    model_result = pd.DataFrame(df)  # DUMMY RESULT, CHANGE

    # Equality check
    gt_result_sorted = gt_result.sort_values(by=gt_result.columns.tolist()).reset_index(
        drop=True
    )
    model_result_sorted = model_result.sort_values(
        by=model_result.columns.tolist()
    ).reset_index(drop=True)
    results.append(
        (gt_result_sorted.equals(model_result_sorted), database, row["query_category"])
    )

    result_df = pd.DataFrame(
        results, columns=["eqauality", "database", "query_category"]
    )

    result_df.to_csv(os.path.join(path, "results.csv"), encoding="utf-8", index=False)
