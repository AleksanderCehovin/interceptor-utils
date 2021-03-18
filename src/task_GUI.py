# Emulated Interceptor GUI Receiver
# Connects PULL socket to tcp://localhost:PORT
# Collects and prints data from a data processing pipeline 
# over the socket determined by PORT..
#
# Useful for debugging to check that a data processing
# pipeline is actually sending over the channel.
#

import sys
import time
import zmq


PORT=5557

context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:{}".format(PORT))
receiver.bind("tcp://*:{}".format(PORT))


# Process tasks forever
while True:
    s = receiver.recv_string()

    sys.stdout.write("Rx: " + s + "\n")
    sys.stdout.flush()

    # Do the work
    time.sleep(0.01)

