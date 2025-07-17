from causalbench.modules import Dataset, Metric, Model, Context, Run

def main():
    context: Context = Context(module_id=19, version=1)

    run: Run = context.execute()
    print(run)


if __name__ == '__main__':
    main()
