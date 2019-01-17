from __future__ import unicode_literals
from prompt_toolkit.shortcuts import prompt
from auth import check_env, get_env_values

def user_prompt():
    prm = ''
    if check_env():
        user = get_env_values()
        prm = '(' + user['username'] + ')>>> '
    prompt(prm)
    return prm
    