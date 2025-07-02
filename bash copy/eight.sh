#!/bin/bash
# eight.sh
# sed and streams
# standard input = standard input stream
# standard output, standard error
# typically textual

# sed 's/search-pattern/replacement-string/flags'
# sed replaces just the first instance in a line by default
# add 'g' flag to replace all instances in a line
# can use a numeric index in flag instead to specify index within line
# sed -i.{input_file} {string pattern} {oiutput file}
