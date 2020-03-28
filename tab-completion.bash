#/usr/bin/env bash
_session_completions()
{
  if [ "${COMP_WORDS[COMP_CWORD-1]}" == "-i" ]
  then
    local IFS=$','
    COMPREPLY=($(compgen -W "$(python3 main.py -k)"))
  elif [ "${COMP_WORDS[COMP_CWORD-1]}" == "-s" ] || [ "${COMP_WORDS[COMP_CWORD-1]}" == "-r" ] || [ "${COMP_WORDS[COMP_CWORD-1]}" == "-n" ]
  then
    local IFS=$','
    COMPREPLY=($(compgen -W "$(python3 main.py -n)"))
  fi

}

complete -F _session_completions session