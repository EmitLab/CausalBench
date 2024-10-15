from causalbench.modules import Metric

metric_web = Metric(module_id=1, version=1)
metric_path = metric_web.fetch()
metric_web = Metric(zip_file=metric_path)
assert metric_web.type=="metric", "Metric could not be fetched from web."

metric_local = Metric(zip_file='metric/accuracy_static.zip')
assert metric_local.type=="metric", "Metric could not be fetched from web."
#metric_local.publish(public=True)