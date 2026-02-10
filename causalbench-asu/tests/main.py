from bunch_py3 import Bunch
from causalbench.modules import Dataset, Metric, Model, Context, Run, Task

def main():
    pass

    task = Task(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/task/regression.zip").load()

    dataset = Dataset(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/data/california_housing.zip")
    data_files = dataset.load()

    # model = Model(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/model/linear_regression.zip")
    # out = model.execute(Bunch({'data': data_files.file1.copy(deep=True), 'fit_intercept': True, 'positive': False, 'helpers': task.helpers()}))
    
    model = Model(zip_file="C:/Users/prata/Files/Git/CausalBench/causalbench-asu/tests/model/decision_tree_regressor.zip")
    out = model.execute(Bunch({'data': data_files.file1.copy(deep=True), 'criterion': 'squared_error', 'splitter': 'best', 'max_depth': None, 'min_samples_split': 2, 'min_samples_leaf': 1, 'ccp_alpha': 0.0, 'random_state': None, 'helpers': task.helpers()}))

    print()
    print()
    print()
    print('[Predicted]')
    print(out.output.prediction.data)

    print()
    print()
    print()
    print('[Ground Truth]')
    print(data_files.file1.copy(deep=True).data)
    
    # # model
    # print('[MODEL]')
    # data = data_files.file1.copy(deep=True)

    # target = task.helpers().get_target(data).copy(deep=True)
    # target[:] = 0

    # print(task.helpers().get_target(data))

    # task.helpers().set_target(data, target)
    # print(task.helpers().get_target(data))

    # print()
    # print()
    # print()

    # print('[METRICS]')
    # ground_truth = data_files.file1.copy(deep=True)
    # predicted = data

    # target = task.helpers().get_target(ground_truth)
    # print(target)

    # target = task.helpers().get_target(predicted)
    # print(target)

    # print()

    # features = task.helpers().get_features(ground_truth)
    # print(features)

    # features = task.helpers().get_features(predicted)
    # print(features)

    # task: Task = Task(module_id=1, version=1)
    # # print(task.name)
    # task.publish(public=True)

    # dataset: Dataset = Dataset(zip_file="C:\\Users\\prata\\Files\\Git\\CausalBench\\causalbench-asu\\tests\\data\\abalone.zip")
    # dataset.publish()

    # dataset: Dataset = Dataset(module_id=1, version=1)
    # # # print(dataset.name)
    # dataset.publish(public=True)

    # task: Task = Task(zip_file="C:\\Users\\prata\\Files\\Git\\CausalBench\\causalbench-asu\\tests\\task\\discovery.static.zip")
    # task.publish()

    # model: Model = Model(zip_file="C:\\Users\\prata\\Files\\Git\\CausalBench\\causalbench-asu\\tests\\model\\pc.zip")
    # model.publish()

    # model: Model = Model(module_id=1, version=1)
    # # # print(model.name)
    # model.publish(public=True)

    # metric: Metric = Metric(zip_file="C:\\Users\\prata\\Files\\Git\\CausalBench\\causalbench-asu\\tests\\metric\\accuracy_static.zip")
    # metric.publish()

    # metric: Metric = Metric(module_id=1, version=1)
    # # print(metric.name)
    # metric.publish(public=True)

    # context: Context = Context.create(
    #     name='Context1',
    #     description='Test static context',
    #     task=task,
    #     datasets=[(dataset, {'data': 'file1', 'ground_truth': 'file2'})],
    #     models=[(model, {})],
    #     metrics=[(metric, {})])
    
    # context.publish()
    
    # # run: Run = context.execute()
    # # print(run)


if __name__ == '__main__':
    main()
