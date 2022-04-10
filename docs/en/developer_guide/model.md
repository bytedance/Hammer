# Introduce Models

There is a principle when writing Model: **the model can be easily used without the Hammer framework**. 
That is to say, it is best not to have dependencies between different models, even if there are shared blocks between different models. 
**Compatibility and flexibility** is the primary consideration when writing a model.

## Steps

1. New a Python file under `models/`, and write the network structure in the file as usual. Note that if you encounter a shared block with existing projects, make a copy to this file;
2. Register the model in `models/__init__.py`;
3. Invoke `build_model()` to build an instance of the model and test whether it works as expected.

## Practical Advice

1. Try not to refer to any network structures in other local files;
2. Distinguish which parameters are related to the model itself, and which are not (and take them out). A common problem is that the parameters related to calculating loss are also included;
3. Distinguish which parameters are required to initialize the model (written in `__init__()`) and which only need to be provided at runtime (written in `forward()`).