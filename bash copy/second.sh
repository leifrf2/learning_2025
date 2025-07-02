#!/bin/bash

# exit status 0 to 255
# 0 is success, anything else is an error
# $? contains the return code of the previously executed command

ls /not/here
echo "$?"

HOST="google.com"
ping -c 1 $HOST
if [ "$?" -eq "0" ]
then
    echo "$HOST reachable."
else
    echo "$HOST unreachable."
fi

HOST="google.com"
ping -c 1 $HOST
if [ "$?" -ne "0" ]
then
    echo "$HOST unreachable."
fi

HOST="google.com"
ping -c 1 $HOST
RETURN_CODE=$?

if [ "$RETURN_CODE" -eq "0" ]
then
    echo "$HOST is reachable."
fi

# chain commands with && for and and || for OR and ;
# && = only if previous is 0
# || = only if previous is non-0
# ; = always execute (same as separate line)


echo "next"
HOST="google.com"
ping -c 1 $HOST && echo "$HOST unreachable."

# exit 0
# exit 1
# exit 255
# sets $? to the value after exit
# will exit script immediately and return that value

