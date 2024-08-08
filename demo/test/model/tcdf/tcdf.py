#import tcdf
#import runTCDF
import pandas
import numpy
import subprocess

file = 'runTCDF.py'
def execute(data, space, arguments):
# check if `data` is dataframe
    if not isinstance(data, pandas.DataFrame):
        raise TypeError("data must be a DataFrame object")

    # the model does not take space, it should be type none.
    if space is not None:
    #if not isinstance(space, None):
        raise TypeError("This model does not support space.")
    arguments = arguments
    if arguments is None:
        #means no arguments are provided, proceed using data as usual.

        #TODO: TCDF takes in the file location instead of the data. Needs workaround.
        #TODO: TCDF requires at least one argument, which is the data.
        #TODO: TCDF's results need to be seperated into analysis and results parts. Requires a parser.
        #args = ["--data", "test/model/tcdf/tcdfmodule/misc/data/demo_dataset.csv"]
        command = ['python', 'runTCDF.py', '--data', data]
        #pred_output = runTCDF(data=data)
    else:
        command = ['python', 'runTCDF.py', '--data', data, '--kernel_size', arguments.get('kernel_size'),
                   '--dilation_coefficient', arguments.get('dilation_coefficient'), '--significance', arguments.get('significance'),
                   '--epochs', arguments.get('epochs')]


    #pred_output = runTCDF(data=data, args=args)

    execution = subprocess.run(command, capture_output=True, text=True)
    #Output parser: outs var1, var2, tau
    #stdout_text = proc.stdout.decode('utf-8')
    #stderr_text = proc.stderr.decode('utf-8')

    # Define the pattern to match
    pattern = r"(\w+) causes (\w+) with a delay of (\d+) time steps\."

    # Find all matches using regex
    matches = re.findall(pattern, stdout_text)

    # Print the matches
    for match in matches:
        # Remove the '=' sign
        print(f"{match[0]} causes {match[1]} with a delay of {match[2]} time steps.")

    # check if returned data type is graph/adjacency matrix
    if isinstance(pred_output, numpy.ndarray) or isinstance(pred_output, pandas.DataFrame):
        # Check if it's a square matrix for adjacency matrix
        if len(pred_output.shape) == 2 and pred_output.shape[0] == pred_output.shape[1]:
            print("result is an adjacency matrix")
        else:
            print("result is not an adjacency matrix")
    else:
        print("result is neither a numpy array nor a pandas DataFrame")


#   return {'pred': }
