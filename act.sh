#!/bin/bash

# Copyright (C) 2012 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause

# Description
# Runs the activate function and evaluates its results
# Based on the __conda_activate shell function in conda.sh

# if [ -n "${CONDA_PS1_BACKUP:+x}" ]; then
#     # Handle transition from shell activated with conda <= 4.3 to a subsequent activation
#     # after conda updated to >= 4.4. See issue #6173.
#     PS1="$CONDA_PS1_BACKUP"
#     \unset CONDA_PS1_BACKUP
# fi
# \local ask_conda
# ask_conda="$(PS1="${PS1:-}" __conda_exe "$@")" || \return

# # error: 
# # __conda_exe: command not found
# # return: can only `return' from a function or sourced script


# CONDA_EXE=$CONDA_PREFIX/bin/conda

__conda_exe() (
    "$CONDA_EXE" $_CE_M $_CE_CONDA "$@"
)

ask_conda="$(PS1="${PS1:-}" __conda_exe shell.posix activate abc)" || \return

# ask_conda="conda activate abc"
# ask_conda="conda shell.posix activate abc"

\eval "$ask_conda"

# PS1='(abc) '
# export PATH='/Users/kca/miniconda3/envs/abc/bin:/Users/kca/miniconda3/condabin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/MacGPG2/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin'
# export CONDA_PREFIX='/Users/kca/miniconda3/envs/abc'
# export CONDA_SHLVL='1'
# export CONDA_DEFAULT_ENV='abc'
# export CONDA_PROMPT_MODIFIER='(abc) '
# export CONDA_EXE='/Users/kca/miniconda3/bin/conda'
# export _CE_M=''
# export _CE_CONDA=''
# export CONDA_PYTHON_EXE='/Users/kca/miniconda3/bin/python'

# __conda_hashr

if [ -n "${ZSH_VERSION:+x}" ]; then
    \rehash
elif [ -n "${POSH_VERSION:+x}" ]; then
    :  # pass
else
    \hash -r
fi