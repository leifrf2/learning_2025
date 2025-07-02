import threading
import time
import concurrent.futures

# Problem:
# print an increasing counter
# until the user presses enter

done = False

def worker(text):
    counter = 0
    while not done:
        time.sleep(1)
        counter += 1
        print(f"{text}: counter {counter}")


def do_something(seconds):
    print(f"Sleeping {seconds} seconds...")
    time.sleep(seconds)
    return f"Done Sleeping... {seconds}"

# just pass the function to invoke
# if daemon=True, this thread terminates if the parent thread terminates
# if daemon=False, it will keep going and check done value again
worker_threads = [
    threading.Thread(target=worker, daemon=True, args=("ABC",)),
    threading.Thread(target=worker, daemon=True, args=("XYZ",))
]

# creates an executor object which we can check on the status of 
# the execution
with concurrent.futures.ThreadPoolExecutor() as executor:
    running_executors = [executor.submit(do_something, i) for i in range(5, 0, -1)]

    for f in concurrent.futures.as_completed(running_executors):
        print(f.result())

    # this applies do_something for everything in range
    # and return results in the order they were started
    # waits until all results are done
    map_results = executor.map(do_something, range(5, 0, -1))
    
    for result in map_results:
        print(result)

    # if the function hits an exception
    # the result is only raised when the result is retrieved
    # NOT when the function is executed

    # wait on the executor to complete and collect the output



#for worker_thread in worker_threads:
#    worker_thread.start()


