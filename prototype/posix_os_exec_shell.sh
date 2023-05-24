#!/bin/sh

# Author: Katherine Chen Abrikian
# Date Created: 2023-05-03
# Last Modified: 2023-05-21

# Description
# Used for testing use of the arguments list in os.execve.
# Print out each supplied argument to the command line in a new line
# Evaluate each argument in sequence
# Run a new instance of the default shell specified in the environment variables

# Usage
# posix_os_exec_shell

# Print each argument on a new line
for arg in "$@"
do
    echo "$arg"
done

# Evaluate all the arguments at once
eval "$@"

echo PS1=${PS1}

PS1="(habanero) "
export PS1
# The hash command must be called to get it to forget past
# commands. Without forgetting past commands the $PATH changes
# we made may not be respected
hash -r 2>/dev/null
echo PS1=${PS1}

# run an interactive instance of the user's default shell to complete activation
# new shell will inherit the environment variables of this process
${SHELL}

exit 0