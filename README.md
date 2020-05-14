# 2048-AI

This is an application of temporal difference learning for the game *2048*. The current repo is in need of clean
up (TODO). This implementation uses linear functions of state features and neural networks to approximate
the state value function for TDL. Since it uses a separate function or network for each action, it is akin
to Q-learning.

## Dependencies

Without CUDA
- Python 3.7.2
- TensorFlow 2.2.0 : `python -m pip install tensorflow==2.2.0`
- NumPy 1.17.2 : `python -m pip install numpy`

With CUDA
- Python 3.7.2
- TensorFlow-gpu 2.2.0 : `python -m pip install tensorflow-gpu==2.2.0`
- NumPy 1.17.2 : `python -m pip install numpy`
- CUDA 10.1 (10.2 probably won't work!)
- CUDA Toolkit (forgot version, 10.1 probably)
- CUDA capable GPU

I have not tested it without CUDA enabled so I cannot make any guarantees about the functionality of it.
Installing with the `pip` commands above should work but I cannot guarantee it.

## How to Run

An old version with linear parameterized functions for value function approximation is found in 
[2048-linear_parameterized](2048-linear_paramaterized). The current root contains the neural network value 
function approximaters.

For both versions, to run just do `python q-learn.py`. Files may take some manual attunement to work how you
might expect (I did not ensure correctness of files after I finished getting the data I needed).

NOTE: Do not run the current `q-learn.py` expecting it to terminate. It will take on the order of days
or weeks to finish. You can still run it to see some potential scores of the agent. At any rate you can always
hit `ctrl+C` to terminate.