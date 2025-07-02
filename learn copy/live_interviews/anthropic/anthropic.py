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
    result_events: List[Event] = list()

    # just compare previous stack and this stack


    # we want to return end events
    # before start events

    # an end event is defined as
    # we do not find an existing element in the next sample

    # we traverse down the call stack
    # as soon as we hit a new function
    # that means everything at or below this level in the previous call stack
    # terminated (in unwinding order)
    # that similarly means that everything below this in the current/new call stack
    # has started (in winding order) == top-down

    if len(samples) == 0:
        return list()
    
    if len(samples) >= 1:
        # just return start events for everything
        sample = samples[0]
        result_events.extend([
            Event(kind='start', ts=sample.ts, name=element) for element in sample.stack
        ])

    for i in range (1, len(samples)):
        previous_sample = samples[i - 1]
        current_sample = samples[i]

        k = 0
        while k < len(previous_sample.stack):
            # what about when there are an unequal number of elements
                
            if k >= len(current_sample.stack) or previous_sample.stack[k] != current_sample.stack[k]:
                # we hit a difference
                # need to start ending functions under this element
                # start from the end of what's running
                # and terminate them up until this point
                #TODO: check off-by-one
                for j in range(len(previous_sample.stack) - 1, k, -1):
                    # end events
                    result_events.append(
                        Event(
                            kind='end',
                            ts=current_sample.ts,
                            name=previous_sample.stack[j]
                        )
                    )
        

            # now we start all the new ones
            # no op if current_sample is smaller
            for j in range(k, len(current_sample.stack)):
                result_events.append(
                    Event(
                        kind='start',
                        ts=current_sample.ts,
                        name=current_sample.stack[k]
                    )
                )
                
            k += 1

        # just adding here to fire end events
        # for what no longer exists in current_sample
        # but exists in previous_sample


        if k < len(current_sample.stack):
            # we've started all of these new
            result_events.extend(
                [Event(kind='start',name=element,ts=current_sample.ts) for element in current_sample.stack[k:]]
            )

    return result_events


# expected_result = [Event('start',7.5,'main'), Event('start', 9.2, 'my_fn'), Event('end', 10.7, 'my_fn'), Event_start_my_fn_2]

if __name__=="__main__":
    samples = [Sample(7.5, ["main"]), Sample(9.2, ["main", "my_fn"]), Sample(10.7, ["main"])]
    traces = convert_to_trace(samples) 
    expected_result = [Event('start',7.5,'main'), Event('start', 9.2, 'my_fn'), Event('end', 10.7, 'my_fn')]

    pprint(traces)