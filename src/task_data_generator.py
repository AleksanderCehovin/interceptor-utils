# Mockup data processing pipeline.
# Binds PUSH socket to tcp://localhost:5557
# Sends data to a GUI via a socket. The data
# format is adapted to the GUI in the Interceptor
# MX package, and that GUI application should be
# able to receive this stream.
#


import zmq
import time
import math
import random

#Total number of data points. I think this data
#allocated memory on the GUI side, don't go astronomical
#with this variable.
N=150000

#Number of data points per run
RUN_LENGTH=15000

#Maximum number of runs. Each run generates a tab in the GUI, which
#allocates memory. Don't set this to astronomical values.
MAX_NO_RUNS=10

#Rate of indexed frames as a modulo number 
INDEXED_RATE=20

#Port number for stream socket
PORT=5557

# Sleep time between frames. Main parameter for effective FPS.
SLEEP_S = 0.005

# STD OUT PRINT INTERVAL
PRINT_INT_FRAMES = 500

def get_spot_number(index,period):
    return int(10000*abs(math.sin(index/period)))

def get_res(index,period):
    value = math.sin(index/period)
    return 5*abs(value*value*value)

def get_quality(index,period):
    value = math.cos(index/period)
    return 100*abs(value*value)

try:
    raw_input
except NameError:
    # Python 3
    raw_input = input

#0MQ context
context = zmq.Context()

# Setup socket for communication
sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:{}".format(PORT))
print("******************************************\n")
print("Pipeline connected to tcp://localhost:{}\n".format(PORT))
print("******************************************\n")

#Wait for user confirmation before starting to push data
print("Press Enter when the GUI is ready: ")
_ = raw_input()
print("Sending data to GUI...")

#Send a data string N times to GUI
run_no=0
img_no=0
fps_counter=1
fps_time_start = time.time()
for i in range(0,N):
    #Set up a new run which generates a new tab in GUI
    if img_no % RUN_LENGTH == 0 and run_no <= MAX_NO_RUNS:
        run_no += 1 
        img_no = 0 # Reset image counter each new run
        period = random.randint(100,500)
    #Check if frame is indexed (True) or not (NA)
    indexed="NA"
    if img_no % INDEXED_RATE == 0:
        indexed="True"
    #Generate data for no. spots, resolution, and quality for every frame
    no_spots=get_spot_number(img_no,period)
    hres = get_res(img_no,period)
    quality = get_quality(img_no,period)
    #Define message string to be sent to GUI. This is the Interceptor GUI format.
    data=u"run {} frame {} result  {} {} {} {} {} {} {} {}  mapping {}".format(run_no,img_no,no_spots,4,quality,hres,7,8,indexed,10,11)
    sender.send_string(data)
    img_no+=1    
    #Handle FPS count
    fps_counter += 1
    if fps_counter % PRINT_INT_FRAMES == 0:
        deltaT = time.time() - fps_time_start
        print("FPS:{:.2f}".format(fps_counter/deltaT))
        fps_time_start = time.time()
        fps_counter = 0
    time.sleep(SLEEP_S)
# Give 0MQ time to deliver
time.sleep(1)
