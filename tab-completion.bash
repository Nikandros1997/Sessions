#!/usr/bin/env bash
_session_completions()
{
  local prev="${COMP_WORDS[COMP_CWORD-1]}"
  COMPREPLY=()
  if [ ${prev} == "-i" ]; then
    local IFS=$','
    COMPREPLY=($(compgen -W "$(python3 main.py -k)"))
    return 0
  elif [[ ${prev} == "-s" || ${prev} == "-r" || ${prev} == "-n" ]]; then
    local IFS=$','
    COMPREPLY=($(compgen -W "$(python3 main.py -n)"))
    return 0
  fi

}

complete -F _session_completions session