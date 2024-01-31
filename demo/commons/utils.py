from commons import executor


def execute_and_report(module_path, function_name, /, *args, **keywords):
    try:
        response = executor.execute(module_path, function_name, *args, **keywords)

        print('-' * 80)
        print(f'Module: {module_path}')
        print()

        print('Output:')
        print(response["output"])
        print()

        print(f'Duration: {response["duration"]} nanoseconds')
        print(f'Used Memory: {response["memory"]} bytes')
        if response["gpu_memory"] is None:
            print(f'Used GPU Memory: None')
        else:
            print(f'Used GPU Memory: {response["gpu_memory"]} bytes')
        print()

        print(f'Python: {response["python"]}')
        print(f'Imports: {response["imports"]}')
        print()

        print(f'Platform: {response["platform"]}')
        print(f'Processor: {response["processor"]}')
        print(f'GPU: {response["gpu"]}')
        print(f'Architecture: {response["architecture"]}')
        print(f'Total Memory: {response["memory_total"]} bytes')
        if response["gpu_memory_total"] is None:
            print(f'Total GPU Memory: None')
        else:
            print(f'Total GPU Memory: {response["gpu_memory_total"]} bytes')
        print(f'Total Storage: {response["storage_total"]} bytes')
        print('-' * 80)

        return response["output"]
    except FileNotFoundError as e:
        print(e)
    except AttributeError as e:
        print(e)
