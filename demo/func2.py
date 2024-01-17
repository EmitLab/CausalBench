from time import sleep
import numpy as np
import pandas as pd

def foo(num1, num2):
    sleep(0.1)

    mult = 0
    for i in range(num1):
        mult += num2

    return mult, num1 * num2, num1 / num2
