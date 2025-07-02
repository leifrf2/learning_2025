#!/bin/bash
# case statements

# case "$1" in
#   start)
#       /usr/sbin/sshd
#       ;;
#   stop)
#       kill $(cat /var/run/sshd.pid)
#       ;;

# matches are case-sensitive
# wildcards are useful for default,
# otherwise behavior is to continue
# can match multiple options with a pipe, like this:
# start|START)
# [yY] | [yY] [eE] [sS] matches y, Y, or any combination of YES

case "$VAR" in
    pattern_1)
        # commands
        ;;
    pattern_N)
        # commands
        ;;
esac

