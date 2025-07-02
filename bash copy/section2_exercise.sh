#!/bin/bash

MY_VAR="Shell Scripting is Fun!"
echo $MY_VAR

HOSTNAME=$(hostname)
echo "This script is running on $HOSTNAME"

SHADOW="/etc/shadow"

if [ -e $SHADOW ]
then
    echo "Shadow passwords enabled"
fi

if [ -w $SHADOW ]
then 
    echo "You have permissions to edit $SHADOW"
else
    echo "You do NOT have permissions to edit $SHADOW"
fi

ANIMALS="man bear pig dog cat sheep"
for ANIMAL in $ANIMALS
do
    echo $ANIMAL
done

for PROMPT in $@
do
    if [ -f $PROMPT ]
    then
        echo "this is a file"
        ls -l $PROMPT
    elif [ -d $PROMPT ]
    then
        echo "this is a directory"
        ls -l $PROMPT
    else
        echo "this is something else"
    fi
done
