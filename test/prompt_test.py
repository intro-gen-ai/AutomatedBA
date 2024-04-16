import pandas as pd
import os
from src.core.driver import layoutProcess
from src.util import SnowflakeManager, ControlDict
path = os.path.dirname(os.path.realpath(__file__))
"""
OUTPUT KEY:
-1 = snowflake connection error
0 = success
1 = table created but it is incorrect
2 = SQL compliation error / table not created
"""
converter = ControlDict()
df = pd.read_csv(os.path.join(path, 'test_data_working.csv'))

sample_size = 15
df = df.sample(sample_size)


snowflake = SnowflakeManager()
result = []
for p_ind in range(1,31):
    prompt_result = [os.path.basename(converter.convert('p', str(p_ind)))]

    success_count = 0
    completion_count = 0
    
    for index, row in df.iterrows():
        gt_success = False
        gpt_success = False
        database = row['db_name']
        question = row['question']
        gt_query = row['query']
        try:
            snowflake.connect(database.upper())
            
        except:
            prompt_result.append(-1)
            continue
    

        try:

            gt_result = snowflake.query_df(gt_query)
            if isinstance(gt_result, pd.DataFrame):
                gt_success = True
            
        except:
        
            pass
    

        try:

            response, model_result = layoutProcess('1', '1', str(p_ind), str(p_ind), '1', question,database.upper())
            if isinstance(model_result, pd.DataFrame):
                gpt_success = True
        except:
            pass


        if gt_success and gpt_success:
            completion_count +=1
            gt_result_sorted = gt_result.sort_values(by=gt_result.columns.tolist()).reset_index(drop=True)
            model_result_sorted = model_result.sort_values(by=model_result.columns.tolist()).reset_index(drop=True)
            if gt_result_sorted.equals(model_result_sorted):

                
                success_count +=1
                prompt_result.append(0)
                print("success")
            else:
                
                prompt_result.append(1)

        else:
            
            prompt_result.append(2)
    
    prompt_result.append(completion_count/sample_size)
    prompt_result.append(success_count/sample_size)
    result.append(tuple(prompt_result))


result_df = pd.DataFrame(result)

result_df.to_csv(os.path.join(path, 'prompt_experiment_results.csv'), encoding='utf-8', index=False)
df.to_csv(os.path.join(path, 'prompt_exeriment_sampled_tests.csv'), encoding='utf-8', index=False)