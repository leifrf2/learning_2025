import sys
from dataclasses import dataclass
from typing import Dict, List, Tuple
import heapq

"""
Overview
A "job" is a programming task that runs unattended. 
Suppose you have a list of jobs and you can spawn workers that can execute the jobs. 
Given a list of jobs for the next day and the amount of time each job takes to run, 
create a scheduler that schedules the jobs such that you complete all of them using the least number of workers possible.

The following are the specifications for the job scheduler:

Once a worker is created, it can be used for as many jobs as you want, but can only work on one job at a time.
The job scheduler should pick the worker with the lowest index if there are multiple workers available.
Workers are assigned an index, starting at 0 for the first worker, 1 for the second, and so on.
The following describes the format of the input:

Number of jobs to run N
Followed by N lines each with the start time <start-time:string> of the job and the time taken <duration:integer> by the job to complete.
start-time is provided in the 24-hour format. For example, 0323, 0014, 2359 are all valid start times.
The unit for duration is minutes. A job starting at 0323 and taking 122 minutes will end at 0525 and the worker running the job will be free to run a new job at 0526.
The following describes the format of the output:

The first line is the minimum number of workers used.
Followed by N lines each with the job identifier <job-identifier:string> and the worker identifier <worker-identifier:string> that ran the job, sorted by job identifiers.
<job-identifier> the index of the job prefixed with J.
<worker-identifier> is the index of the worker that ran the job prefixed with W.
Finally, please note that the number of jobs could be up to 1440 (minutes in a day).

Notes

Assume that the input will never be malformed.
Assume that all the jobs defined in the input will start and end in a single day (meaning that they will run between 0000 hours to 2359 hours).
Assume that no two jobs will have the same start time.
The job definitions in the input are unordered.
Sample Input
10
0000 30
0015 16
0020 11
0030 10
0031 12
0040 10
0045 5
0051 11
0059 1
0058 2
Sample Output
4
J0 W0
J1 W1
J2 W2
J3 W3
J4 W0
J5 W1
J6 W0
J7 W0
J8 W2
J9 W1
"""

@dataclass
class Job:
    start_time: int
    duration: int

    def calc_end_time(self) -> int:
        return self.start_time + self.duration


def ingest_file(filename: str) -> List[Job]:
    jobs: List[Job] = list()
    with open(filename, 'r') as f:
        num_jobs: int = int(f.readline())

        for _ in range(num_jobs):
            # should have 2 elements
            line_split = f.readline().split(' ')

            # convert to minutes-in-day (1440)
            start_time_minutes: int = int(line_split[0][:2]) * 60 + int(line_split[0][2:])
            duration_minutes: int = int(line_split[1])

            jobs.append(Job(
                start_time=start_time_minutes,
                duration=duration_minutes
            ))
        
    return jobs


def print_format_job_worker_pair(job_id: int, worker_id: int) -> None:
    print(f"J{job_id} W{worker_id}")


# job_id, worker_id return
def assign_jobs(jobs: List[Job]) -> List[Tuple[int, int]]:
    jobs.sort(key=lambda j: j.start_time)

    job_assignments: List[Tuple[int, int]] = list()

    # as we assign jobs to workers
    # we know which one will be done next
    # and when the next assignment is coming up
    # so we need to keep track of completing jobs
    # and pending jobs

    # maintain a sorted list of active jobs
    # maintain a sorted list of pending jobs
    # run the scheduling loop on pending jobs

    available_worker_heap: List[int] = list()
    heapq.heapify(available_worker_heap)

    max_worker_count: int = -1

    # free_time, worker_index
    active_workers: List[Tuple[int, int]] = list()
    heapq.heapify(active_workers)

    # on loop:
        # check timestamp of next job to start
        # complete active jobs between last loop time and this start time
        # assign this job to the lowest index free worker
        # track the max active worker count

    for job_index, job_to_schedule in enumerate(jobs):
        current_time = job_to_schedule.start_time
        
        while len(active_workers) > 0:
            if active_workers[0][0] < current_time:
                heapq.heappush(available_worker_heap, heapq.heappop(active_workers)[1])
            else:
                break

        if len(available_worker_heap) == 0:
            max_worker_count += 1
            heapq.heappush(available_worker_heap, max_worker_count)
            # assign max_worker_count

        lowest_available_worker_index: int = heapq.heappop(available_worker_heap)
        heapq.heappush(active_workers, (job_to_schedule.calc_end_time(), lowest_available_worker_index))
        job_assignments.append((job_index, lowest_available_worker_index))


    return job_assignments


def main(filename: str):
    jobs_to_schedule: List[Job] = ingest_file(filename)
    assigned_jobs = assign_jobs(jobs_to_schedule)
    worker_count = max(j[1] for j in assigned_jobs) + 1

    print(worker_count)
    for job in assigned_jobs:
        print_format_job_worker_pair(job[0], job[1])

if __name__=="__main__":
    filename = \
        "lyft_laptop/jobscheduler_sample_input.txt" \
        if len(sys.argv) < 2 \
        else sys.argv[1]
    main(filename)
