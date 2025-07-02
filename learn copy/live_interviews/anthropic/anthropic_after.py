from pprint import pprint
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Sample:
    ts: float
    stack: list[str]

@dataclass
class Event:
    kind: str # either 'start' or 'end'
    ts: float
    name: str

def convert_to_trace(samples: list[Sample]) -> list[Event]:
    if len(samples) == 0:
        return list()

    if len(samples) == 1:
        sample=samples[0]
        return [Event(kind='start',ts=sample.ts,name=name) for name in sample.stack]

    # at least 2 elements in samples
    result_events: List[Event] = list()

    # record the firsts tep
    result_events.extend(Event(
            kind='start',
            name=fn,
            ts=samples[0].ts) for fn in samples[0].stack
    )

    # record all the incremental steps
    for i in range(1, len(samples)):
        previous = samples[i - 1]
        current = samples[i]

        diff_index = 0
        while len(previous.stack) > diff_index and len(current.stack) > diff_index \
            and previous.stack[diff_index] == current.stack[diff_index]:
            diff_index += 1

        # at this point there are no more similar ones

        # end all the running processes in unwinding order
        result_events.extend(Event(
                    kind='end',
                    name=fn,
                    ts=current.ts
                ) for fn in reversed(previous.stack[diff_index:]))

        # start all newly running processes in winding order

        result_events.extend(Event(
            kind='start',
            name=fn,
            ts=current.ts
        ) for fn in current.stack[diff_index:])

    return result_events

if __name__=="__main__":
    samples = [Sample(7.5, ["main"]), Sample(9.2, ["main", "my_fn"]), Sample(10.7, ["main"])]
    traces = convert_to_trace(samples) 
    expected_result = [Event('start',7.5,'main'), Event('start', 9.2, 'my_fn'), Event('end', 10.7, 'my_fn')]

    pprint(traces)


"""
part 1

Problem: Converting stack samples to a trace
Sampling profilers are a performance analysis tool for finding the slow parts of your code by periodically sampling the entire call stack. In our problem the samples will be a list of Samples of a float timestamp and a list of function names, in order by timestamp.

Sample stacks contain every function that is currently executing
The stacks are in order from outermost function (like "main") to the innermost currently executing function
An unlimited amount of execution/change can happen between samples. We don't have all the function calls that happened, just some samples we want to visualize.
"""


"""
part 2

Sometimes our samples will just be on some tiny leaf function that executes for a minimal amount of time but they'll show up in the trace.
What if we pruned it down by only emitting events for function calls that appear in N consecutive samples for configurable N?

You still need to emit consistent events, and use the same definition for what constitutes a single call as in the first part.
There are many very different working solutions but they're all inspired by similar insights as the previous part.

You can decide if you want to use the 1st or Nth timestamp for the start time of your events.
"""
