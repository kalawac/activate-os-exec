# Copyright (C) 2012 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause
import os
import argparse

from conda.base.context import context
from conda.cli.main import init_loggers
from conda.activate import PosixActivator
from conda.exceptions import ArgumentError

import conda.plugins


def get_activate_builder(activator):
    '''
    create dictionary containing the environment variables to be set, unset and exported,
    as well as the package activation and deactivation scripts to be run 
    '''
    print("Plugin: Build cmds_dict...")

    if activator.stack:
        builder_result = activator.build_stack(activator.env_name_or_prefix)
    else:
        builder_result = activator.build_activate(activator.env_name_or_prefix)
    return builder_result

def activate(activator, cmds_dict):
    '''
    change environment. as a new process in in new environment, run deactivate
    scripts from packages in old environment (to reset env variables) and
    activate scripts from packages installed in new environment.
    '''
    print("Plugin: In activate...")

    path = "/Users/kca/dev-conda/activate-os-exec/prototype/posix_os_exec_shell.sh"
    arg_list = [path]
    env_map = os.environ

    # for PosixActivator process, no unset vars and only var that is set is prompt
    # this method ignores them for now
    export_path = cmds_dict.get("export_path", {}) # seems to be empty for posix shells
    export_vars = cmds_dict.get("export_vars", {})

    print(f"{export_path=}")
    print(f"{export_vars=}")

    for key, value in sorted(export_path.items()):
        env_map[str(key)]=str(value)
    
    for key, value in sorted(export_vars.items()):
        env_map[str(key)]=str(value)

    print(env_map)

    deactivate_scripts = cmds_dict.get("deactivate_scripts", ())

    if deactivate_scripts:
        deactivate_list = [(activator.run_script_tmpl % script) + activator.command_join for script in deactivate_scripts]
        arg_list.extend(deactivate_list)

    activate_scripts = cmds_dict.get("activate_scripts", ())

    if activate_scripts:
        activate_list = [(activator.run_script_tmpl % script) + activator.command_join for script in activate_scripts]
        arg_list.extend(activate_list)

    os.execve(path, arg_list, env_map)

def deactivate_scripts(activator, cmds_dict, env):
    '''
    run deactivate scripts from packages installed into the existing environment prior to activating new environment
    '''
    print("Plugin: In deactivate_scripts...")

    path = "/Users/kca/dev-conda/activate-os-exec/prototype/posix_os_exec_shell.sh"
    arg_list = [path]
    activate_command = f"conda ppws activate_pt2 {env}"

    # for some reason, putting . in front of the local scripts causes an error: "No such file or directory"
    # they run fine if they're just called by path
    # the real package scripts seem to run with the ., though

    deactivate_scripts = cmds_dict.get("deactivate_scripts", ())
    deactivate_list = [(activator.run_script_tmpl % script) + activator.command_join for script in deactivate_scripts]

    # deactivate_scripts = ("/Users/kca/dev-conda/activate-os-exec/sum.sh 3 6", "~/learning/bash-mastery/sum_nums")
    # deactivate_list = [script + activator.command_join for script in deactivate_scripts]

    if deactivate_list:
        arg_list.extend(deactivate_list)

    arg_list.append(activate_command)

    # confirming that commands calling conda directly work
    # arg_list.append("conda -h\n")
    # arg_list.append("conda info --envs")
    # arg_list.append(f"conda shell.posix activate ${env}")

    os.execv(path, arg_list)


def raise_invalid_command_error(actual_command=None):
            message = (
                "'activate', 'deactivate', or 'reactivate'"
                "command must be given"
            )
            if actual_command:
                message += ". Instead got '%s'." % actual_command
            raise ArgumentError(message)


def posix_plugin_with_shell(*args, **kwargs):
    # package deactivation scripts need to run in old environment, before rest of activation process is run
    print("Plugin: In ppws...")

    # argparse handles cleanup but I need to check if the UTF-8 issue might still persist
    # no need to check for missing command - handled by argparse
    # env_args = tuple(ensure_text_type(s) for s in env_args) 
    parser = argparse.ArgumentParser(
    description="Process conda activate, deactivate, and reactivate")
    parser.add_argument("ppws", type=str, nargs=1, help="this package's entry point")
    parser.add_argument("command", metavar="c", type=str, nargs=1,
                    help="the command to be run: 'activate', 'deactivate' or 'reactivate'")
    parser.add_argument("env", metavar="env", default=None, type=str, nargs="?",
                    help="the name or prefix of the environment to be activated")

    args = parser.parse_args()

    command = args.command[0]
    env = args.env
    print(f"{env=}")

    context.__init__()
    init_loggers(context)

    if command not in  ("activate", "deactivate", "reactivate"):
        raise_invalid_command_error(actual_command=command)

    env_args = (command, env) if env else (command,)
    
    activator = PosixActivator(env_args)

    # call the methods leading up to the command-specific builds
    activator._parse_and_set_args(env_args)

    # at the moment, if activate is called without an environment, reactivation is being run
    # through conda's normal process because this process would be called during '_parse_and_set_args'
    # this can be dealt with later by editing the '_parse_and_set_args' method
    # or creating a new version for the plugin

    if command == 'activate' and env:
        # using redefined activate process instead of _Activator.activate
        cmds_dict = get_activate_builder(activator)
        activate(activator, cmds_dict)
    elif command == 'activate' and not env:
        # activate without an environment specified is actually reactivate
        cmds_dict = activator.build_reactivate()

    #TODO: look into deactivation process and see what's going on here; it's not working
    # can we just exit the sub-shell? If so, how do we do that?
    # is deactivation in this context actually activation of the previous environment?
    if command == 'deactivate':
        cmds_dict = activator.build_deactivate()

    if command == 'reactivate':
        cmds_dict = activator.build_reactivate()




@conda.plugins.hookimpl
def conda_subcommands():
    yield conda.plugins.CondaSubcommand(
        name="ppws",
        summary="Plugin for POSIX shells that calls the conda processes used for activate, deactivate, and reactivate",
        action=posix_plugin_with_shell
    )