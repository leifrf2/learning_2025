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

@dataclass
class TraceEntry:
    name: str
    sample_start: int
    start_emitted: bool

def convert_to_trace(samples: list[Sample], n: int) -> list[Event]:
    if len(samples) < n:
        return list()

    if len(samples) == 0:
        return list()
    
    # TODO handle too-few cases of n vs len(sample)

    # at least 2 elements in samples
    result_events: List[Event] = list()

    stack_history: List[TraceEntry] = [
        TraceEntry(name=fn, sample_start=0, start_emitted=False)
        for fn in samples[0].stack
    ]

    # record all the incremental steps
    for i in range(1, len(samples)):
        current = samples[i]

        for entry in stack_history:
            if i - entry.sample_start >= n and not entry.start_emitted:
                # then this one has been here long enough to emit
                result_events.append(
                    Event(
                        kind='start',
                        ts=samples[entry.sample_start].ts,
                        name=entry.name
                    )
                )

                # not sure if this is needed, but keep for now
                entry.start_emitted = True

        diff_index = 0
        while len(stack_history) > diff_index and len(current.stack) > diff_index \
            and stack_history[diff_index].name == current.stack[diff_index]:
            diff_index += 1

        # at this point there are no more similar ones

        # end all the running processes in unwinding order
        result_events.extend(Event(
                    kind='end',
                    name=entry.name,
                    ts=current.ts
                ) for entry in reversed(stack_history[diff_index:]) if entry.start_emitted)

        stack_history = stack_history[:diff_index]

        # start all newly running processes in winding order

        stack_history.extend(TraceEntry(
            name=fn,
            start_emitted=False,
            sample_start=i
        ) for fn in current.stack[diff_index:])

    return result_events

if __name__=="__main__":
    #samples = [Sample(7.5, ["main"]), Sample(9.2, ["main", "my_fn"]), Sample(10.7, ["main"])]
    samples_2 = [Sample(7.5, ["main"]), Sample(9.2, ["main", "my_fn", "foo"]), Sample(10.7, ["main", "my_fn"]), Sample(11.5, [])]
    traces = convert_to_trace(samples_2, 4)
    expected_result = [Event('start',7.5,'main'), Event('start', 9.2, 'my_fn'), Event('end', 10.7, 'my_fn')]

    pprint(traces)


"""
Sometimes our samples will just be on some tiny leaf function that executes for a minimal amount of time but they'll show up in the trace.
What if we pruned it down by only emitting events for function calls that appear in N consecutive samples for configurable N?

You still need to emit consistent events, and use the same definition for what constitutes a single call as in the first part.
There are many very different working solutions but they're all inspired by similar insights as the previous part.

You can decide if you want to use the 1st or Nth timestamp for the start time of your events.
"""
