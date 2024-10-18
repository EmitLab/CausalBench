from causalbench.modules import Run
from causalbench.modules.context import Context
from causalbench.modules.dataset import Dataset
from causalbench.modules.model import Model
from causalbench.modules.metric import Metric
from unittest.mock import patch

def mock_input(prompt):
    if 'y' in prompt.lower() or 'n' in prompt.lower():
        return 'y'  # Automatically answer "Y" to yes/no prompts
    return 'y'  # Default response in other cases

'''===Config===
These are the id's of models.
Will need to be updated one last time after the initial population has been done.
'''
#datasets
sachs = 1422
telecom = 1424
time_sim = 2
adult = 16
fashion_minst = 6
abalone = 1

#these are for netsim.
gap_min = 17
gap_limit = 1416
step = 25

numbers = list(range(gap_min, gap_limit))

#models
pc_hp = [1,7]
ges_hp = [2,4]

varlingam_hp = [4,2]
pcmciplus_hp = [3,2]

#metrics
acc_stat = 1
f1_stat = 2
prec_stat = 8
recall_stat = 10

acc_stat, f1_stat, prec_stat, recall_stat

shd_stat = 12 # is broken atm

prec_temp = 9
recall_temp = 11
acc_temp = 3
shd_temp = 4
f1_temp = 6

temporal_db = [time_sim]#, telecom]
temporal_model = [varlingam_hp, pcmciplus_hp]
temporal_metric = [prec_temp, recall_temp, acc_temp, f1_temp] #, shd_temp]

static_db = [abalone, adult, sachs]#, fashion_minst]
static_model = [ges_hp, pc_hp]
static_metric = [acc_stat, f1_stat, prec_stat, recall_stat] #, shd_stat]
#static_db = static_db+numbers
#===Config===

#Creation of sets:
#stat_all_dataset_set = [(Dataset(module_id=num, version=1),{'data': 'file1', 'ground_truth': 'file2'}) for num in static_db]
temp_all_dataset_set = [(Dataset(module_id=num, version=1),{'data': 'file1', 'ground_truth': 'file2'}) for num in temporal_db]

stat_model_set = [(Model(module_id=num[0], version=num[1]), {}) for num in static_model]
temp_model_set = [(Model(module_id=num[0], version=num[1]), {}) for num in temporal_model]

stat_metric_set = [(Metric(module_id=num, version=1), {}) for num in static_metric]
temp_metric_set = [(Metric(module_id=num, version=1), {}) for num in temporal_metric]


#Creation of contexts
# print("temp context create-publish")
# temp_context: Context = Context.create(name='Temporal Benchmark',
#                                     description='This context runs currently available temporal models and metrics with available datasets.',
#                                     task='discovery.temporal',
#                                     datasets=temp_all_dataset_set,
#                                     models=temp_model_set,
#                                     metrics=temp_metric_set)
# temp_context.publish() #id 8



# Create a for loop to iterate in ranges based on the step size
iter = 0
for start in range(gap_min, gap_limit, step):
    end = min(start + step, gap_limit)  # Calculate the end of the range, ensure it doesn't exceed gap_limit
    static_db = list(range(start, end))   # Create the sublist for the current range
    stat_all_dataset_set = [(Dataset(module_id=num, version=1), {'data': 'file1', 'ground_truth': 'file2'}) for num in
                            static_db]
    static_context: Context = Context.create(name='Net Dataset Static Benchmark Items ' + str(iter*25) + ' - ' + str(iter*25 + 25),
                                        description='This context runs currently available static models and metrics with available datasets.',
                                        task='discovery.static',
                                        datasets=stat_all_dataset_set,
                                        models=stat_model_set,
                                        metrics=stat_metric_set)
    with patch('builtins.input', mock_input):
        static_context.publish(public=True) #id 12


