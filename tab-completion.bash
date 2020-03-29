#!/usr/bin/env bash
_session_completions()
{
  # cd '/Users/nikandrosmavroudakis/Documents/Projects/Session'
  local prev="${COMP_WORDS[COMP_CWORD-1]}"
  COMPREPLY=()
  if [ ${prev} == "-i" ]; then
    local IFS=$','
    COMPREPLY=($(compgen -W "$(python3 ~/Documents/Projects/Session/main.py -k)"))
    return 0
  elif [[ ${prev} == "-s" || ${prev} == "-r" || ${prev} == "-n" ]]; then
    local IFS=$','
    COMPREPLY=($(compgen -W "$(python3 ~/Documents/Projects/Session/main.py -n)"))
    return 0
  fi

}

complete -F _session_completions session