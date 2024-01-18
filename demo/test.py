import executor


def call_func(module_path):
    num1 = 1
    num2 = 2

    function_name = 'foo'

    try:
        response = executor.execute(module_path, function_name, num1=num1, num2=num2)

        print('-' * 80)
        print(f'Module: {module_path}')
        print()
        print(f'Output: {response["output"]}')
        print(f'Duration: {response["duration"]} nanoseconds')
        print(f'Memory: {response["memory"]} bytes')
        print()
        print(f'Python: {response["python"]}')
        print(f'Imports: {response["imports"]}')
        print()
        print(f'Platform: {response["platform"]}')
        print(f'Processor: {response["processor"]}')
        print(f'GPU: {response["gpu"]}')
        print(f'Architecture: {response["architecture"]}')
        print(f'Virtual Memory: {response["virtual_memory"]} bytes')

        if response["gpu_memory"] is None:
            print(f'GPU Memory: None')
        else:
            print(f'GPU Memory: {response["gpu_memory"]} bytes')

        print(f'Storage: {response["storage"]} bytes')
        print('-' * 80)
    except FileNotFoundError as e:
        print(e)
    except AttributeError as e:
        print(e)


if __name__ == '__main__':
    call_func("./func1.py")
    call_func("./func2.py")
