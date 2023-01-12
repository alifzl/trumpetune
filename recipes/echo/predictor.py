# Do the required imports
import os
import time


def predictor(input_list, batch_size=1):
    output_list = []
    while input_list:
        input_batch = input_list[:batch_size]
        input_list = input_list[batch_size:]
        output_list += input_batch
    
    return output_list
