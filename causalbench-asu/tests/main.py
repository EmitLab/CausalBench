from bunch_py3 import Bunch
from causalbench.modules import Dataset, Metric, Model, Context, Run, Task

def main():
    pass

    # task = Task(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/task/classification.zip").load()
    # task = Task(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/task/regression.zip").load()

    # # dataset = Dataset(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/data/breast_cancer_wisconsin.zip")
    # # dataset = Dataset(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/data/forest_covertype.zip")

    # # dataset = Dataset(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/data/california_housing.zip")
    # dataset = Dataset(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/data/diabetes.zip")

    # data_files = dataset.load()

    # # model = Model(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/model/logistic_regression.zip")
    # # out = model.execute(Bunch({'data': data_files.file1.copy(deep=True), 'penalty': 'l2', 'C': 1.0, 'l1_ratio': 0.0, 'dual': False, 'tol': 1e-4, 'fit_intercept': True, 'intercept_scaling': 1.0, 'class_weight': None, 'random_state': None, 'solver': 'lbfgs', 'max_iter': 100, 'verbose': 0, 'warm_start': False, 'helpers': task.helpers()}))

    # # model = Model(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/model/decision_tree_classifier.zip")
    # # out = model.execute(Bunch({'data': data_files.file1.copy(deep=True), 'criterion': 'gini', 'splitter': 'best', 'max_depth': None, 'min_samples_split': 2, 'min_samples_leaf': 1, 'min_weight_fraction_leaf': 0.0, 'max_features': None, 'random_state': None, 'max_leaf_nodes': None, 'min_impurity_decrease': 0.0, 'class_weight': None, 'ccp_alpha': 0.0, 'helpers': task.helpers()}))

    # model = Model(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/model/linear_regression.zip")
    # out = model.execute(Bunch({'data': data_files.file1.copy(deep=True), 'fit_intercept': True, 'tol': 1e-6, 'positive': False, 'helpers': task.helpers()}))
    
    # # model = Model(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/model/decision_tree_regressor.zip")
    # # out = model.execute(Bunch({'data': data_files.file1.copy(deep=True), 'criterion': 'squared_error', 'splitter': 'best', 'max_depth': None, 'min_samples_split': 2, 'min_samples_leaf': 1, 'min_weight_fraction_leaf': 0.0, 'max_features': None, 'random_state': None, 'max_leaf_nodes': None, 'min_impurity_decrease': 0.0, 'ccp_alpha': 0.0, 'helpers': task.helpers()}))

    # print()
    # print()
    # print()
    # print('[Predicted]')
    # print(out.output.prediction.data)

    # print()
    # print()
    # print()
    # print('[Ground Truth]')
    # print(data_files.file1.copy(deep=True).data)

    # # metric = Metric(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/metric/accuracy_classification.zip")
    # # out = metric.evaluate(Bunch({'ground_truth': data_files.file1.copy(deep=True), 'prediction': out.output.prediction, 'normalize': True, 'sample_weight': None, 'helpers': task.helpers()}))

    # # metric = Metric(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/metric/precision_classification.zip")
    # # out = metric.evaluate(Bunch({'ground_truth': data_files.file1.copy(deep=True), 'prediction': out.output.prediction, 'labels': None, 'pos_label': 1, 'average': 'macro', 'sample_weight': None, 'zero_division': 0, 'helpers': task.helpers()}))

    # # metric = Metric(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/metric/mae_regression.zip")
    # # out = metric.evaluate(Bunch({'ground_truth': data_files.file1.copy(deep=True), 'prediction': out.output.prediction, 'sample_weight': None, 'multioutput': 'uniform_average', 'helpers': task.helpers()}))

    # metric = Metric(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/metric/r2score_regression.zip")
    # out = metric.evaluate(Bunch({'ground_truth': data_files.file1.copy(deep=True), 'prediction': out.output.prediction, 'sample_weight': None, 'multioutput': 'uniform_average', 'helpers': task.helpers()}))

    # print()
    # print()
    # print()
    # print('[Score]')
    # print(out.output.score)




    # task1 = Task(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/task/classification.zip", module_id=4, version=1)
    
    # dataset1 = Dataset(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/data/breast_cancer_wisconsin.zip")
    # dataset2 = Dataset(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/data/forest_covertype.zip")

    # model1 = Model(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/model/logistic_regression.zip")
    # model2 = Model(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/model/decision_tree_classifier.zip")

    # metric1 = Metric(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/metric/accuracy_classification.zip")
    # metric2 = Metric(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/metric/precision_classification.zip")

    # context1 = Context.create(
    #     name='Classification 1',
    #     description='Test classification context',
    #     task=task1,
    #     datasets=[(dataset1, {'data': 'file1', 'ground_truth': 'file1'}),
    #               (dataset2, {'data': 'file1', 'ground_truth': 'file1'})],
    #     models=[(model1, {}), (model2, {})],
    #     metrics=[(metric1, {}), (metric2, {})]
    # )

    # run1 = context1.execute()

    # print(run1)



    # task2 = Task(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/task/regression.zip", module_id=5, version=1)
    
    # dataset3 = Dataset(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/data/california_housing.zip")
    # dataset4 = Dataset(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/data/diabetes.zip")

    # model3 = Model(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/model/linear_regression.zip")
    # model4 = Model(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/model/decision_tree_regressor.zip")

    # metric3 = Metric(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/metric/mae_regression.zip")
    # metric4 = Metric(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/metric/r2score_regression.zip")

    # context = Context.create(
    #     name='Regression 1',
    #     description='Test classification context',
    #     task=task2,
    #     datasets=[(dataset3, {'data': 'file1', 'ground_truth': 'file1'}),
    #               (dataset4, {'data': 'file1', 'ground_truth': 'file1'})],
    #     models=[(model3, {}), (model4, {})],
    #     metrics=[(metric3, {}), (metric4, {})]
    # )

    # run2 = context.execute()

    # print(run2)




if __name__ == '__main__':
    main()
