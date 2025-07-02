#!/bin/bash
# fourth.sh
# wildcards

# char or string for pattern patching

# ca[nt]*
# can, cat, candy, catch
# [aeiou] - matches any of these chars exactly once
# [!aeiou]* - matches all files which do not start with these chars
# [a-g]* - matches all strings starting with a,b,c,d,e,f,g
# [3-6]* - matches all strings starting with 3,4,5,6
# [[:alnum:]] - matches all alphanumeric characters
# alpha, digit, lower, space, upper are also pre-defined
# \ - escape char
# *\? - matches all strings ending with a question mark

echo "Choose a file extension - .csv .html .txt .py"
read EXTENSION
echo "Extension: $EXTENSION"

DATE_STR=$(date +%Y%m%d)

echo "Choose an output prefix (press enter for $DATE_STR)"
read PREFIX

if [ ! $PREFIX ]
then
    PREFIX=$DATE_STR
else
    PREFIX="${PREFIX}-"
fi

echo $PREFIX

DEST_DIR="../files_2"

for FILE in $(ls *${EXTENSION})
do
    echo "found $FILE"
    NEW_FILE="${DEST_DIR}/${PREFIX}${FILE}"
    cp $FILE $NEW_FILE
done

exit 0