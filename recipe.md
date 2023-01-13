# What is a Recipe?

- In order to serve a model via trumpetune, files `example.py`, `predictor.py` and optional `requirements.txt`, `extras.sh` needs to be added to our existing python scripts (a.k.a ML codes).


# predictor.py

```python
# OUR MODEL CODE GOES HERE

def predictor.py(list_of_inputs, batch_size=1):
    # inputs can be python objects (string/list/dict..) (text models) or file_paths (image/speech models)
    # run prediction on list of inputs here
    # batch_size is the optional batch_size param you can pass to your keras/tensorflow/pytorch model
    # You can ignore batch_size and loop over list_of_inputs and and predict one by one too
    # output shoud be JSON serializable (strings/lists/dicts/ints/floats ..)
    
    return list_of_outputs
    
```


# example.py

```python
example = [INPUT]
# INPUT can be string/lsit/dict (REST API will accept JSON) anything your scripts need.
# INPUT can also be file path (in which case the REST API will accept multi-part posts), in which case you can keep example file next to example.py and INPUT = example file name
```
