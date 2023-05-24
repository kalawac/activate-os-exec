#!/bin/sh

PS1="(Yo yo yo) "
export PS1
# The hash command must be called to get it to forget past
# commands. Without forgetting past commands the $PATH changes
# we made may not be respected
hash -r 2>/dev/null
echo PS1=${PS1}

/Users/kca/miniconda3/envs/abc/bin/conda ppws activate newscratch