
def convert_to_trace(samples: list[Sample]) -> list[Event]:
    # call_stack_level -> fn_name
    running_functions: Dict[int, str] = {}
    result_events: List[Event] = list()

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




    for sample in samples:
        # start with end events
        # TODO: double check the return sorting of dictionary.items() and keys()
        for index, fn in running_functions.items():
            sample_functions = sample.stack

            if len(sample_functions) < index or sample_functions[index] != fn:
                # we know that the previous function at this index has changed
                result_events.append(Event(
                    kind='end',
                    name=fn,
                    ts=sample.ts
                ))
            # implicit else:
                # if it is the same function name
                # then it's still running
                # no action needed
        
        # next to start events
        for sample_index, sample_fn in enumerate(sample.stack):
            if sample_index in running_functions.keys():
                if running_functions[sample_index] != sample_fn:
                    result_events
                    # there's still something running at this level in the call stack
                    # but it's a different function



    raise Exception("unimplemented")

samples = [Sample(7.5, ["main"]), Sample(9.2, ["main", "my_fn"]), Sample(10.7, ["main", "my_fn_2"])]
convert_to_trace(samples) # expected_result = [Event('start',7.5,'main'), Event('start', 9.2, 'my_fn'), Event('end', 10.7, 'my_fn'), Event_start_my_fn_2]

# logic
# samples are already sorted by time
# from that, we can expect the first time we see somethign to always be the start event
# then the first time we don't see it is its end event

# we need to maintain the "active" set
# start = first see it
# end = first don't see it

# we maintain a set of the functions running now
# if we don't see an element form this set in the next sample, then we know it was torn down
# and we emit an end event

