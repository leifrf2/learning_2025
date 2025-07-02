#!/bin/bash
TEST_VAR="test"
set -x
echo $TEST_VAR
set +x
hostname

# debugging
# adding -x will print the line being executed
# adding -e will exit on error
# adding -v will print command exactly as they appear
# can be combined, i.e. #!/bin/bash -ex

set -ex
FILE_NAME="/not/here"
ls .
#ls $FILE_NAME
ls .
echo $FILE_NAME
set +ex

echo
echo
echo

set -v
TEST_VAR="test"
echo "$TEST_VAR"
set +v

# you can create a ≠your own debugging tools
# use a special variable to you, i.e. DEBUG

DEBUG=true
if $DEBUG
then
    echo "Debug mode ON."
else
    echo "Debug mode OFF."
fi

$DEBUG && echo "Debug mode ON (pipe)."
$DEBUG || echo "Debug mode OFF (pipe)."

$DEBUG_ECHO="echo"
$DEBUG_ECHO ls

function debug() {
    echo "Executing: $@"
    $@
}

debug ls