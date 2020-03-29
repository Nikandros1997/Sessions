#!/usr/bin/env bash
_session_completions()
{
  local main_path="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
  local prev="${COMP_WORDS[COMP_CWORD-1]}"
  COMPREPLY=()
  if [ ${prev} == "-i" ]; then
    local IFS=$','
    COMPREPLY=($(compgen -W "$(python3 ${main_path}/main.py -k)"))
    return 0
  elif [[ ${prev} == "-s" || ${prev} == "-r" || ${prev} == "-n" ]]; then
    local IFS=$','
    COMPREPLY=($(compgen -W "$(python3 ${main_path}/main.py -n)"))
    return 0
  fi

}

complete -F _session_completions session