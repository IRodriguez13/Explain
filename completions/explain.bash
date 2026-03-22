# bash completion for explain (explain-errors)
# Instalación: copiar a ~/.local/share/bash-completion/completions/explain
#   o: source /ruta/al/repo/completions/explain.bash
# Requiere bash ≥4 (asociativos opcionales; funciona sin _init_completion).

_explain_complete() {
  local cur prev words cword
  if declare -F _get_comp_words_by_ref &>/dev/null; then
    _get_comp_words_by_ref -n : cur prev words cword
  else
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD - 1]}"
  fi

  local langs='auto C C++ Assembly C# Python JavaScript Rust'
  # Opciones de explain (mantener alineado con explain.cli:construir_parser).
  local flags='-h --help --version -l --lang -v --verbose --full --ub-hints -nw --no-warnings --max-warnings -m --match --shell -cnt --count'

  case "$cur" in
    --lang=*)
      COMPREPLY=($(compgen -W "$langs" -- "${cur#--lang=}"))
      return
      ;;
    -l=*)
      COMPREPLY=($(compgen -W "$langs" -- "${cur#-l=}"))
      return
      ;;
  esac

  case "$prev" in
    -l | --lang)
      COMPREPLY=($(compgen -W "$langs" -- "$cur"))
      return
      ;;
    -m | --match)
      COMPREPLY=($(compgen -f -- "$cur"))
      return
      ;;
    --shell)
      return
      ;;
    --max-warnings)
      COMPREPLY=($(compgen -W '1 3 5 10 20 50 100' -- "$cur"))
      return
      ;;
  esac

  if [[ $cur == -* ]]; then
    COMPREPLY=($(compgen -W "$flags" -- "$cur"))
    return
  fi

  compopt -o default 2>/dev/null || true
  COMPREPLY=($(compgen -c -- "$cur"))
}

complete -F _explain_complete explain
