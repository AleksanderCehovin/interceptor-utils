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

#Connection port to feeding process
PORT=5557

#Sleep time between collection attempts
SLEEP_S = 0

#Print all frames?
PRINT_ALL = False
PRINT_DELIM = "***************************************************"

#Print Interval in frames
PRINT_INT_FRAMES = 500



context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:{}".format(PORT))
receiver.bind("tcp://*:{}".format(PORT))

fps_counter = 0
fps_time_start = time.time()
# Process tasks forever
while True:
    s = receiver.recv_string()

    if PRINT_ALL:
        #For high frame rates it's a bad idea
        #sys.stdout.write("Rx: " + s + "\n")
        #sys.stdout.flush()
        pass

    fps_counter += 1
    if fps_counter % PRINT_INT_FRAMES == 0:
        deltaT = time.time() - fps_time_start
        sys.stdout.write("FPS:{:.2f}\n".format(fps_counter/deltaT))
        if not PRINT_ALL:
            sys.stdout.write("Rx: " + s + "\n" + PRINT_DELIM + "\n")
        sys.stdout.flush()
        fps_time_start = time.time()
        fps_counter = 0

    # Do the work
    time.sleep(SLEEP_S)

