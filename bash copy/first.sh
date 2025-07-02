#!/bin/bash

# notes

# shebang
# "shebang" = #! (sharp + bang)
# shebang tells the interpreter to execute the path after the shebang
# no shebang = command is executed in current shell
#!/usr/bin/python will do python

# variables
# VARIABLE_NAME="Value"
# no spaces
# case sensitive (convention they are all upper case)
# $MY_VARIABLE to reference variable
# ALSO ${MY_VARIABLE}, to reference inline
# i.e. echo "${MY_VARIABLE}ing" prints value of MY_VARIABLE immediately followed by 'ing'
# OUTPUT=$(my_command)

# conditions
# [condition-to-test-for]
# [ -e /etc/passwd ] = "file /etc/passwd exists"
#
# -z STRING = true if empty
# -n STRING = true if not empty
# STRING1 = STRING2 equality
# STRING1 != STRING2 inequality
#
# num1 -eq num2 = equality
# num1 -ne num2 = inequality
# num1 -lt num2 = less than
# num1 -le num2 = less than or equal
# num1 -gt num2 = greater than
# num1 -ge num2 = greater than or equal

# man {function} = help

MY_SHELL="bash"

if [ "$MY_SHELL" = "bash" ]
then
    echo "You seem to like the bash shell."
elif ["$MY_SHELL" = "not bash"]
then
    echo "You seem to like the bash shell."
else
    echo "You seem to like some other shell."
fi

# for VAR in ITEM_1 ITEM_N
# do
    # command 1
    # command 2
    # command N
# done

for COLOR in red green blue
do
    echo "COLOR: $COLOR"
done

COLORS="red green blue"
for COLOR in $COLORS
do
    echo "COLOR: $COLOR"
done

# argument names
# $0 = this file name
# $1 = parameter 1, $2 = param 2, etc

# STDIN
# read -p "PROMPT" VARIABLE
# *** This doesn't work in my terminal?

