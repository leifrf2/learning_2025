import anthropic
from anthropic import Sample, convert_to_trace, Event

def test_1():
    samples = [Sample(7.5, ["main"]), Sample(9.2, ["main", "my_fn"]), Sample(10.7, ["main", "my_fn_2"])]

def test_2():
    samples = [Sample(7.5, ["main"]), Sample(9.2, ["main", "my_fn"]), Sample(10.7, ["main"])]
    traces = convert_to_trace(samples) 
    expected_result = [Event('start',7.5,'main'), Event('start', 9.2, 'my_fn'), Event('end', 10.7, 'my_fn')]

    assert traces == expected_result


# test case
example_samples = [Sample(7.5, ["main","my_outer_function","my_inner_function"])]
example_samples = [Sample(7.5, ["main","my_outer_function_2","my_inner_function"])]
