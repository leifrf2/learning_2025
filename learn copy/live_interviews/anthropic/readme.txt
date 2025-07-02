
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

