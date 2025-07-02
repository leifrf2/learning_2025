#!/bin/bash
# sixth.sh
# logging

# syslog standard
# var/log/messages
# var/log/syslog

# facilities: kern, user, mail, daemon, auth, local[0-7]
# severities: emerg, alert, crit, err, warning, notice, info, debug

# logger -p local0.info "Message"
#           ^ facility
#                  ^ severity
#                       ^ severity
# include pid with "-i" option

# can include tags as well, like with -t


# while loops
# while [ condition_is_true ]
# do
#   command_1
#   command_N
# done

# while [ "$CORRECT" != "y" ]
# do
#     read -p "Enter your name:" NAME
#     echo $NAME
#     CORRECT="y"
# done

FILE_PATH=$1
NUM_LINES=$2

LINE_NUM=1
while read LINE
do
    echo "${LINE_NUM}: $LINE"
    ((LINE_NUM++))

    if [ -n "$NUM_LINES" ] && [ $LINE_NUM -gt $NUM_LINES ]
    then
        break
    fi
done < $FILE_PATH

echo "=== next ==="

ls -l | while read LINE
do
    echo "listed: $LINE"
done

echo "=== next ==="

ls -l | while read A B C
do
    echo "listed: A:$A B:$B C:$C"
done

echo "sleeping for 1"
sleep 1
echo "sleep over"

echo "Choose 1: show disk usage, 2: show uptime, 3: show who. Choose q to quit"

while true
do
    echo "What would you like to do?"
    read INPUT

    case "$INPUT" in
        1)
            df
            echo
            ;;
        2)
            uptime
            echo
            ;;
        3)
            who
            echo
            ;;
        q)
            break
            ;;
    esac
done

echo "Goodbye!"
exit 0

# continue and break work in bash as expected

