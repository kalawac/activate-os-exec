import os
import sys


from conda.common.compat import ensure_text_type
from conda.base.context import context
from conda.cli.main import init_loggers
from conda.activate import PosixActivator

import conda.plugins


def handle_env(*args, **kwargs):
    # cleanup argv
    env_args = sys.argv[2:]  # drop executable/script and sub-command
    env_args = tuple(ensure_text_type(s) for s in env_args)

    context.__init__()
    init_loggers(context)

    # specify activator child class directly
    activator = PosixActivator(env_args)

    # run methods leading up to finalize

    def _yield_commands(cmds_dict):
        for key, value in sorted(cmds_dict.get("export_path", {}).items()):
            yield self.export_var_tmpl % (key, value)

        for script in cmds_dict.get("deactivate_scripts", ()):
            yield self.run_script_tmpl % script

        for key in cmds_dict.get("unset_vars", ()):
            yield self.unset_var_tmpl % key

        for key, value in cmds_dict.get("set_vars", {}).items():
            yield self.set_var_tmpl % (key, value)

        for key, value in cmds_dict.get("export_vars", {}).items():
            yield self.export_var_tmpl % (key, value)

        for script in cmds_dict.get("activate_scripts", ()):
            yield self.run_script_tmpl % script


    path = "/bin/sh" # needs to be the user's location of the shell
    args = (
        "PS1='(plugin) '",
        "export PATH='/Users/kca/miniconda3/envs/plugin/bin:/Users/kca/miniconda3/condabin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/MacGPG2/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin'",
        "export CONDA_SHLVL='1'",
        "export CONDA_PROMPT_MODIFIER='(plugin) '",
        "echo ARDHC complete!"
    )

    # confirm that we're using plugin and not usual conda process
    print("echo ARDHC complete!")
    # execute process
    # process does not return -- what does that mean? will the user have to launch the conda executable to get back?
    op = os.execve(path, env_args, )

@conda.plugins.hookimpl
def conda_subcommands():
    yield conda.plugins.CondaSubcommand(
        name="ardhc",
        summary="Plugin for POSIX shells that calls the conda processes used for activate, deactivate, reactivate, hook, and command",
        action=handle_env,
    )

# def test_osexec():
#     a = "echo supercalifragilisticexpialidocious"

# # my thoughts -- execve bc replace the environment with variable arguments and also have a path
#     op = os.execve()


'''
PS1='(scratch3) '
export PATH='/Users/kca/dev-conda/conda/devenv/Darwin/arm64/envs/devenv-3.8-c/envs/scratch3/bin:/Users/kca/dev-conda/conda/devenv/Darwin/arm64/envs/devenv-3.8-c/bin:/Users/kca/dev-conda/conda/devenv/Darwin/arm64/envs/devenv-3.8-c/condabin:/Users/kca/miniconda3/condabin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/MacGPG2/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin'
export CONDA_PREFIX='/Users/kca/dev-conda/conda/devenv/Darwin/arm64/envs/devenv-3.8-c/envs/scratch3'
export CONDA_SHLVL='2'
export CONDA_DEFAULT_ENV='scratch3'
export CONDA_PROMPT_MODIFIER='(scratch3) '
export CONDA_PREFIX_1='/Users/kca/dev-conda/conda/devenv/Darwin/arm64/envs/devenv-3.8-c'
export CONDA_STACKED_2='true'
export CONDA_EXE='/Users/kca/dev-conda/conda/devenv/Darwin/arm64/envs/devenv-3.8-c/bin/conda'
export _CE_M=''
export _CE_CONDA=''
export CONDA_PYTHON_EXE='/Users/kca/dev-conda/conda/devenv/Darwin/arm64/envs/devenv-3.8-c/bin/python'
. "/Users/kca/dev-conda/conda/devenv/Darwin/arm64/envs/devenv-3.8-c/envs/scratch3/etc/conda/activate.d/hello.sh"
'''

'''
PS1='(plugin) '
export PATH='/Users/kca/miniconda3/envs/plugin/bin:/Users/kca/miniconda3/condabin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/MacGPG2/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin'
export CONDA_SHLVL='1'
export CONDA_PROMPT_MODIFIER='(plugin) '
echo ARDHC complete!
'''