"""
Design a library which writes bytes to a file in a specific order. 
The library should support multi-threading and ensure thread-level ordering.

# Design the following Library:
class DataWriter:
    def __init__(self, file_path_on_disk: str):
        # Constructor to initialize the file path on disk
        self.file_path_on_disk = file_path_on_disk

    def push(self, data: bytes):
        # Method to push data (byte array)
        pass

# Now there is a single-machine server, and your Lib is used by thousands of Threads at the same time. 
# They call the "push" method continuously, so these pushed bytes need your Lib to 
# write to the filePath on disk in the form of append.
# You need to design and fill in the pseudo code so that:

# 1. The data pushed in by each Thread ensures Thread-Level order. For example, 
# Thread_A pushes d1, d2, and Thread_B pushes d3, d4 at the same time. 
# Then the written file content can be d1_d2_d3_d4 or d1_d3_d4_d2, 
# because d1 must be earlier than d2, and d3 must be earlier than d4.
# High throughput, low latency. My understanding is that it is best 
# not to be blocked/wait when each Thread calls push.

# 2. Show how specific bytes of data are written to a disk file.
# 3. Discuss persistence and how to recover from a server crush.
# """
