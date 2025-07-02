#!/bin/bash
# section4_exercise.sh

function file_count_one() {
    echo $(ls -l | wc -l)
}

function file_count() {
    local F=$1
    echo "$F:"
    echo $(ls -l $F | wc -l)
}

file_count /etc
file_count /var
file_count /usr/bin

exit 0