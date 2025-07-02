#!/bin/bash


comm '
echo $1

if [ -f $1 ] 
then
EXIT_STATUS=0
elif [ -d $1 ] 
then
EXIT_STATUS=1
else
EXIT_STATUS=2
fi


echo "This script will exit with a $EXIT_STATUS exit status"
exit $EXIT_STATUS
'

X=$(cat /etc/shadow)
R=$?
if [ $R -eq 0 ]
then
    echo "Command succeeded"
    E=0
else
    echo "Command failed"
    E=255
fi

exit $E

