#!/usr/bin/env bash
# Instala el autocompletado de explain para bash (Ubuntu, Fedora, etc.).
# Uso: desde la raíz del repo:  bash completions/install-bash-user.sh
# Equivalente (instala bash + zsh + fish):  explain --install-shell-completions

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${XDG_DATA_HOME:-$HOME/.local/share}/bash-completion/completions"
mkdir -p "$DEST"
install -m 0644 "$ROOT/completions/explain.bash" "$DEST/explain"
echo "Copiado a: $DEST/explain"
echo "Requisito: paquete bash-completion (sudo apt install bash-completion)."
echo "Cerrá y abrí GNOME Terminal, o ejecutá:  source ~/.bashrc"
echo "Primera vez: escribí «explain » y pulsá Tab (carga diferida), o ejecutá:"
echo "  source $DEST/explain"
echo "Comprobación:  complete -p explain   →  debe mostrar _explain_complete"
