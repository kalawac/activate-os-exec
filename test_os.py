import os
import argparse


parser = argparse.ArgumentParser(
    description='Process conda activate, deactivate, and reactivate')
parser.add_argument('command', metavar='c', type=str, nargs=1,
                    help='the command to be run: activate or deactivate')
parser.add_argument('--env', metavar='env', type=str, nargs=1,
                    help='the name or prefix of the environment to be activated')

args = parser.parse_args()

command = args.command[0]
env = args.env[0] if args.env else None

if command in  ('activate', 'deactivate'):
    print('activating! or deactivating!')

    # path = '/Users/kca/dev-conda/simple-bash-plugin/OLD/sum_nums'
    # arg_list = ['.']

    path = '/Users/kca/dev-conda/activate-os-exec/act.sh'
    # arg_list = ['.']
    # arg_list = ['hello world']
    # os.execv(path, arg_list)

    arg_list=['echo yo']
    env_map = os.environ

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

    env_map['PATH']='/Users/kca/miniconda3/envs/abc/bin:/Users/kca/miniconda3/condabin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/MacGPG2/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin'
    env_map['CONDA_PREFIX']='/Users/kca/miniconda3/envs/abc'
    env_map['CONDA_SHLVL']='1'
    env_map['CONDA_DEFAULT_ENV']='abc'
    env_map['CONDA_PROMPT_MODIFIER']='(abc) '
    env_map['CONDA_EXE']='/Users/kca/miniconda3/bin/conda'
    env_map['_CE_M']=''
    env_map['_CE_CONDA']=''
    env_map['CONDA_PYTHON_EXE']='/Users/kca/miniconda3/bin/python'


    os.execve(path, arg_list, env_map)
else:
    print('oops! I can\'t work with that command!')
    print(os.environ)

# it needs some sort of file
# it can run a shell script but it can't run a python file


# path = "/bin/sh"
# print(os.path.abspath(os.path.expanduser(os.path.expandvars(path))))
# arg_tup = tuple([
#         "PS1='(kca) '",
#         # "export PATH='/Users/kca/miniconda3/envs/plugin/bin:/Users/kca/miniconda3/condabin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/MacGPG2/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin'",
#         # "export CONDA_SHLVL='1'",
#         # "export CONDA_PROMPT_MODIFIER='(plugin) '",
#         "echo ARDHC complete!"
# ])
# os.execv(path, arg_tup)

# is the file actually the actualization logic? and then the arguments are 'eval'?