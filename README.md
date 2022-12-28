# interceptor-utils
The original purpose of this code was for simulation utilities for the Interceptor
GUI at

https://github.com/AleksanderCehovin/interceptor.git

The repository above now includes this simulation code in its repository.

Here, I'm now using it for experiments. Currently I'm testing whether a ZMQ PUSH-PULL 
connection can act as a filtering mechanism when the underlying buffers
are intentionally under-dimensioned to create low frequency preview streams out of
a high-throughput source.
