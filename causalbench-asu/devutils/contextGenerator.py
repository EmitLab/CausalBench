from causalbench.modules import Run
from causalbench.modules.context import Context
from causalbench.modules.dataset import Dataset
from causalbench.modules.model import Model
from causalbench.modules.metric import Metric

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
gap_max = 117
gap_limit = 1416

numbers = list(range(gap_min, gap_max))

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

static_db = [abalone, fashion_minst, adult, sachs]
static_model = [ges_hp, pc_hp]
static_metric = [acc_stat, f1_stat, prec_stat, recall_stat] #, shd_stat]
#static_db = static_db+numbers
#===Config===

#Creation of sets:
stat_all_dataset_set = [(Dataset(module_id=num, version=1),{'data': 'file1', 'ground_truth': 'file2'}) for num in static_db]
temp_all_dataset_set = [(Dataset(module_id=num, version=1),{'data': 'file1', 'ground_truth': 'file2'}) for num in temporal_db]

stat_model_set = [(Model(module_id=num[0], version=num[1]), {}) for num in static_model]
temp_model_set = [(Model(module_id=num[0], version=num[1]), {}) for num in temporal_model]

stat_metric_set = [(Metric(module_id=num, version=1), {}) for num in static_metric]
temp_metric_set = [(Metric(module_id=num, version=1), {}) for num in temporal_metric]


#Creation of contexts
print("temp context create-publish")
temp_context: Context = Context.create(name='Temporal Benchmark',
                                    description='This context runs currently available temporal models and metrics with available datasets.',
                                    task='discovery.temporal',
                                    datasets=temp_all_dataset_set,
                                    models=temp_model_set,
                                    metrics=temp_metric_set)
# temp_context.publish() #id 8

print("static context create-publish")
static_context: Context = Context.create(name='Static Benchmark',
                                    description='This context runs currently available static models and metrics with available datasets.',
                                    task='discovery.static',
                                    datasets=stat_all_dataset_set,
                                    models=stat_model_set,
                                    metrics=stat_metric_set)
static_context.publish() #id 12


