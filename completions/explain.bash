# bash completion for explain (explain-errors)
# Mantener alineado con explain/cli.py → construir_parser().
# Tras actualizar el repo:  bash completions/install-bash-user.sh
#   (sobrescribe ~/.local/share/bash-completion/completions/explain)
#
# Instalación (Ubuntu / Debian / Fedora con bash):
#   mkdir -p ~/.local/share/bash-completion/completions
#   cp explain.bash ~/.local/share/bash-completion/completions/explain
#   # ↑ el archivo DESTINO debe llamarse exactamente «explain» (nombre del comando)
#
# Abrí una terminal nueva o: source ~/.bashrc
#
# bash-completion carga este archivo en DIFERIDO: la primera vez que escribís
# «explain » y pulsás Tab. Antes de eso, «complete -p explain» puede decir que
# no hay especificación (es normal). Para registrar al instante:
#   source ~/.local/share/bash-completion/completions/explain
# Luego: complete -p explain  →  complete -F _explain_complete explain
#
# Si Tab no hace nada: sudo apt install bash-completion y que ~/.bashrc cargue bash_completion.

_explain_complete() {
  local cur prev words cword
  if declare -F _init_completion &>/dev/null; then
    _init_completion -s || return
  elif declare -F _get_comp_words_by_ref &>/dev/null; then
    _get_comp_words_by_ref -n : cur prev words cword
  else
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD - 1]}"
  fi

  local langs='auto C C++ Assembly C# Python JavaScript Rust'
  # Opciones de explain (mantener alineado con explain.cli:construir_parser).
  local flags='-h --help --version -l --lang -v --verbose --full --ub-hints -nw --no-warnings --max-warnings -m --match --shell -cnt --count -f -F --man --man-all -i --input-file --install-shell-completions'
  # Tras las opciones, comandos típicos (evita «compgen -c» vacío = miles de entradas).
  local common_cmds='make ninja cmake meson cargo rustc gcc g++ clang clang++ cc c++ dotnet msbuild csc pytest python3 python pip node npm bun vite tsc'

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
    -i | --input-file)
      COMPREPLY=($(compgen -f -- "$cur"))
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

  # Nunca «compgen -c» con $cur vacío: lista todo el PATH (~miles de nombres).
  if [[ -z "$cur" ]]; then
    case "$prev" in
      explain)
        COMPREPLY=($(compgen -W "$flags" -- "$cur"))
        return
        ;;
      -v | --verbose | --full | --ub-hints | -nw | --no-warnings | -cnt | --count | -h | --help)
        COMPREPLY=($(compgen -W "$common_cmds" -- "$cur"))
        return
        ;;
    esac
    if [[ " $langs " == *" $prev "* ]]; then
      COMPREPLY=($(compgen -W "$common_cmds" -- "$cur"))
      return
    fi
    return 0
  fi

  compopt -o default 2>/dev/null || true
  COMPREPLY=($(compgen -c -- "$cur"))
}

complete -F _explain_complete explain
