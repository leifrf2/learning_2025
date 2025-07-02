#!/bin/bash

# functions must be defined before they are executed
# they can be referenced in text, 
# as long as the function itself is defined befure it is executed

function hello() {
    echo "Hello!"
    now
}

# hello here would not work

function now() {
    echo "It's $(date +%r)"
}

hello

function print-args() {
    for ARG in $@
    do
        echo "$ARG"
    done
}

# by default, all variables are global
# if defined within a function or script, 
# it will be available outside external to that

function print-args-local() {
    local PREFIX="the argument is: "
    for ARG in $@
    do
        echo "${PREFIX}${ARG}"
    done
}

# return in a function block is equivalent to exit in a script
# exit status of the function will be the exit status of 
# the last command executed in the function

# $$ refers to the PID of this script

# leifrf@LC7LGKWJ1C ~/src_personal/bash $ date +%F
# 2024-12-30

