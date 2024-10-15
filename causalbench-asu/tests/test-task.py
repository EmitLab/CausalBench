from causalbench.modules.task import Task

task: Task = Task(module_id='discovery.temporal')
task.load()
assert task.type=="task", "Task could not be fetched from web."
