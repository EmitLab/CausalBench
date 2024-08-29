from causalbench.modules import Run
from causalbench.modules.context import Context

def main():

    # Select and fetch the Context
    context1: Context = Context(module_id=1, version=1)

    # Run selected Context
    run: Run = context1.execute()

    # Print Run execution results
    print(run)

    # Publish the Run
    run.publish()

if __name__ == '__main__':
    main()