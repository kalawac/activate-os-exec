#!/bin/sh

# Author: Katherine Chen Abrikian
# Date Created: 2023-05-03
# Last Modified: 2023-05-10

# Description
# Used for testing use of the arguments list in os.execve. Currently prints out each supplied
# argument to the command line in a new line and and evaluates them all at once.

# Usage
# act

#!/bin/sh

# # Print each argument on a new line
# for arg in "$@"
# do
#     echo "$arg"
# done

# Evaluate all the arguments at once
eval "$@"

exit 0