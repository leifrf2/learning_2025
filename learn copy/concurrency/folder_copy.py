"""
this program finds every file in a given folder
it creates a new file in a given folder containing the metadata for the original file
with the original file name + "_metadata.txt"
"""

import threading
import time
import os
from pathlib import Path
import json
import concurrent.futures
import logging
from typing import Iterable, Optional, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FolderReplicator:
    schedule_interval_s: int = 1

    def __init__(self,
                 origin_folder: str,
                 destination_folder: str,
                 parallelism: int = 10):
        self.origin_folder=origin_folder
        self.destination_folder=destination_folder
        self.parallelism=parallelism

        self.errors_lock: threading.Lock = threading.Lock()
        self.errors: list[str] = list()

        self.available_paths_lock: threading.Lock = threading.Lock()
        self.available_paths_queue: list[str] = [origin_folder]

        self.active_paths_lock: threading.Lock = threading.Lock()
        self.active_paths_set: set[str] = set()

        self.active_threads_lock: threading.Lock = threading.Lock()
        self.active_threads: List[concurrent.futures.Future] = list()

        self.processed_path_counter: int = 0
        self.processed_path_counter_lock : threading.Lock = threading.Lock()

    def increment_processed_path_counter(self) -> None:
        with self.processed_path_counter_lock:
            self.processed_path_counter += 1

    def get_new_path(self, file_path: str) -> str:
        if not file_path.startswith(self.origin_folder):
            raise ValueError(f"file_path must be in origin_folder. {self.origin_folder}, {file_path}")
        
        return self.destination_folder + file_path[len(self.origin_folder):]

    def get_file_metadata(self, file_path: str) -> dict[str, str]:
        file_stats = os.stat(file_path)

        results: dict[str, str] = {
            'file_size' : file_stats.st_size,
            'file_permissions' : oct(file_stats.st_mode)[-3:],
            'creation_time' : time.ctime(file_stats.st_ctime),
            'last_modified_time' : time.ctime(file_stats.st_mtime),
            'last_accessed_time' : time.ctime(file_stats.st_atime)
        }

        return results

    def acquire_path(self) -> Optional[str]:
        with self.available_paths_lock:
            if len(self.available_paths_queue) > 0:
                new_path = self.available_paths_queue.pop(0)
                self.active_paths_set.add(new_path)
                return new_path
            else:
                return None

    def complete_path(self, path: str) -> None:
        with self.active_paths_lock:
            self.active_paths_set.remove(path)

    def extend_queue(self, paths: Iterable[str]) -> None:
        with self.available_paths_lock:
            self.available_paths_queue.extend(paths)
    
    def append_error(self, failed_path: str) -> None:
        with self.errors_lock:
            self.errors.append(failed_path)

    def process_and_complete_path(self, path: str):
        logger.debug(f"executing path {path}")
        if os.path.isfile(path):
            # make file 
            file_metadata = self.get_file_metadata(path)
            destination_path = f"{self.get_new_path(path)}.txt"
            with open(destination_path, 'w') as dp:
                dp.write(json.dumps(file_metadata, indent=4))
        elif os.path.isdir(path):
            # make dir
            destination_path = self.get_new_path(path)
            Path(destination_path).mkdir(parents=True, exist_ok=True)
            self.extend_queue((os.path.join(path, p) for p in os.listdir(path)))
        else:
            logger.debug(f"unknown path type for path: {path}")
            self.append_error(path)
        
        self.complete_path(path)

    # with threadpool, you can create as many threads as you want
    # but they won't start until there is capacity, as set by max_workers
    def start_logged(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.parallelism) as executor:
            while len(self.available_paths_queue) > 0 or any(not t.done() for t in self.active_threads):
                next_path = self.acquire_path()
    
                if not next_path:
                    pass
                    with self.active_threads_lock:
                        pending_threads = 0
                        completed_threads = 0
                        running_threads = 0
                        for t in self.active_threads:
                            if t.running():
                                running_threads += 1
                            elif t.done():
                                completed_threads += 1
                            else:
                                pending_threads += 1
                        logger.info(f"pending: {pending_threads} running: {running_threads} done: {completed_threads}")
                    time.sleep(self.schedule_interval_s)
                else:
                    new_thread = executor.submit(self.process_and_complete_path, next_path)
                    with self.active_threads_lock:
                        self.active_threads.append(new_thread)
        

    def start(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.parallelism) as executor:
            while self.is_potential_work():
                next_path = self.acquire_path()
                if next_path:
                    executor.submit(self.process_and_complete_path, next_path)

    def start_sleep(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.parallelism) as executor:
            while True:
                with self.active_threads_lock:
                    pending_threads = 0
                    completed_threads = 0
                    running_threads = 0
                    for t in self.active_threads:
                        if t.running():
                            running_threads += 1
                        elif t.done():
                            completed_threads += 1
                        else:
                            pending_threads += 1

                logger.info(f"pending: {pending_threads} running: {running_threads} done: {completed_threads}")

                new_thread = executor.submit(time.sleep, 1)
                with self.active_threads_lock:
                    self.active_threads.append(new_thread)

    def start_synchronous(self):
        while len(self.available_paths_queue) > 0:
            next_path = self.acquire_path()
            self.process_and_complete_path(next_path)

    def is_potential_work(self):
        with self.active_paths_lock:
            with self.available_paths_lock:
                return any(self.active_paths_set) or any (self.available_paths_queue)

    def process_path_self(self):
        while self.is_potential_work():
            path = self.acquire_path()
            if path:
                self.process_and_complete_path(path)

    def start_executor_self(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.parallelism) as executor:
            for _ in range(self.parallelism):
                executor.submit(self.process_path_self)

    def start_threading(self):
        threads: List[threading.Thread] = list()
        logger.setLevel(level=logging.DEBUG)

        for i in range(self.parallelism):
            new_thread = threading.Thread(target=self.process_path_self,args=[])
            threads.append(new_thread)
            new_thread.start()

        for thread in threads:
            thread.join()


def main(origin_folder, destination_folder):
    replicator: FolderReplicator = FolderReplicator(origin_folder, destination_folder, 1)
    
    start_time = time.time()
    
    replicator.start_synchronous()
    
    end_time = time.time()
    print(f"took {end_time-start_time:0.4} seconds")

    

if __name__=="__main__":
    origin_folder = os.path.join(Path.home(), "Downloads")

    fc_timestamp = int(time.time())
    destination_folder = os.path.join(Path.home(), "scratch", f"folder_copy_{fc_timestamp}")
    logger.info(f"starting replication from {origin_folder} to {destination_folder}")
    main(origin_folder, destination_folder)

