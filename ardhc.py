import os
import argparse


from conda.common.compat import ensure_text_type
from conda.base.context import context
from conda.cli.main import init_loggers
from conda.activate import PosixActivator
from conda.exceptions import ArgumentError

import conda.plugins

def activate(activator):
    if activator.stack:
        builder_result = activator.build_stack(activator.env_name_or_prefix)
    else:
        builder_result = activator.build_activate(activator.env_name_or_prefix)
    return builder_result

def raise_invalid_command_error(actual_command=None):
            message = (
                "'activate', 'deactivate', or 'reactivate'"
                "command must be given"
            )
            if actual_command:
                message += ". Instead got '%s'." % actual_command
            raise ArgumentError(message)

def ardhc(*args, **kwargs):
    # argparse handles cleanup but I need to check if the UTF-8 issue might still persist
    # no need to check for missing command - handled by argparse
    # env_args = tuple(ensure_text_type(s) for s in env_args) 
    parser = argparse.ArgumentParser(
    description="Process conda activate, deactivate, and reactivate")
    parser.add_argument("ardhc", type=str, nargs=1, help="this package's entry point")
    parser.add_argument("command", metavar="c", type=str, nargs=1,
                    help="the command to be run: 'activate', 'deactivate' or 'reactivate'")
    parser.add_argument("env", metavar="env", default=None, type=str, nargs="?",
                    help="the name or prefix of the environment to be activated")

    args = parser.parse_args()

    command = args.command[0]
    env = args.env

    context.__init__()
    init_loggers(context)

    if command not in  ("activate", "deactivate", "reactivate"):
        raise_invalid_command_error(actual_command=command)
    
    env_args = (command, env) if env else (command,)
    activator = PosixActivator(env_args)

    # call the methods leading up to activate
    activator._parse_and_set_args(env_args)

    # using redefined activate function instead of _Activator.activate
    cmds_dict = activate(activator)

    unset_vars = cmds_dict["unset_vars"]
    set_vars = cmds_dict["set_vars"]
    export_path = cmds_dict.get("export_path", {})
    export_vars = cmds_dict.get("export_vars", {})
    deactivate_scripts = cmds_dict.get("deactivate_scripts", ())
    activate_scripts = cmds_dict.get("activate_scripts", ())

    print("activating! or deactivating!")
    env_map = os.environ

    # ignoring setting and unsetting variables for now
    # TODO: figure out how to set and unset vars :(
    
    
    for key, value in sorted(export_path.items()):
        env_map[str(key)]=str(value)
    
    for key, value in sorted(export_vars.items()):
        env_map[str(key)]=str(value)

    deactivate_list = [activator.run_script_tmpl % script for script in deactivate_scripts]
    activate_list = [activator.run_script_tmpl % script for script in activate_scripts]

    shell_path = env_map["SHELL"]
    exec_shell = f". {shell_path}"


    # TODO: can the deactivate scripts be run as a subprocesses? -- they need to run in the initial environment not the new environment

    # creating the list of arguments to be executed by os.execve
    # minimum argument is to execute the shell
    # order should be deactivate scripts followed by activation followed by activate scripts
    arg_list = []

    # deactivate scripts must be run BEFORE the new environment is activated!
    # the below would take place in the new environment
    # user would have to type in two commands for us to run os.exec twice
    # if deactivate_list:
    #     arg_list.extend(deactivate_list)
    
    arg_list.append(exec_shell)

    if activate_list:
        arg_list.extend(activate_list)

    os.execve(shell_path, arg_list, env_map)

@conda.plugins.hookimpl
def conda_subcommands():
    yield conda.plugins.CondaSubcommand(
        name="ardhc",
        summary="Plugin for POSIX shells that calls the conda processes used for activate, deactivate, and reactivate",
        action=ardhc,
    )