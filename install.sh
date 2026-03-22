#!/usr/bin/env bash
# Instalación / desinstalación de explain-errors en el sistema.
# Uso:
#   sudo ./install.sh              # instala en PREFIX (default: /usr/local)
#   sudo PREFIX=/usr ./install.sh  # binario en /usr/bin, datos en /usr/share
#   sudo ./install.sh uninstall
#   ./install.sh --help
#
# Actualizar: volver a ejecutar ./install.sh (sobrescribe archivos).
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PKGDIR="$ROOT/explain"
MANDIR="$ROOT/man"
MANFILE="$MANDIR/explain.1"

DEFAULT_PREFIX="/usr/local"
PREFIX="${PREFIX:-$DEFAULT_PREFIX}"

die() { echo "install.sh: $*" >&2; exit 1; }

version_from_pyproject() {
  sed -n 's/^version = "\([^"]*\)"/\1/p' "$ROOT/pyproject.toml" | head -n1
}

usage() {
  cat <<EOF
Uso: install.sh [install|uninstall] [--prefix RUTA]

  install     Copia el paquete Python, el lanzador en \$PREFIX/bin/explain,
              la man page y completions (bash/zsh/fish) en
              \$PREFIX/share/explain-errors/completions/ (ver README).
  uninstall   Elimina esos archivos.

Variables:
  PREFIX      Raíz de instalación (default: $DEFAULT_PREFIX)
              Ejemplo: PREFIX=/usr sudo ./install.sh  → /usr/bin/explain

Reinstalar o actualizar: ejecutá de nuevo install (sobrescribe sin preguntar).

Desinstalar:
  sudo ./install.sh uninstall
  (o con el mismo PREFIX que usaste al instalar)
EOF
}

do_install() {
  [[ -d "$PKGDIR" ]] || die "no existe el paquete: $PKGDIR"
  [[ -f "$MANFILE" ]] || die "no existe la man page: $MANFILE"

  local ver
  ver="$(version_from_pyproject)"
  [[ -n "$ver" ]] || die "no pude leer version en pyproject.toml"

  local dest="$PREFIX/share/explain-errors"
  local bin="$PREFIX/bin/explain"
  local man1="$PREFIX/share/man/man1/explain.1"
  local comps="$ROOT/completions"

  install -d "$PREFIX/bin" || die "no se puede escribir en $PREFIX/bin (probá: sudo $0 install)"
  install -d "$dest" || die "no se puede escribir en $dest"
  install -d "$PREFIX/share/man/man1" || die "no se puede escribir en $PREFIX/share/man/man1"

  rm -rf "${dest:?}/explain"
  cp -R "$PKGDIR" "$dest/"

  local man_tmp
  man_tmp="$(mktemp)"
  sed "s/@VERSION@/${ver}/g" "$MANFILE" >"$man_tmp"
  install -m644 "$man_tmp" "$man1"
  rm -f "$man_tmp"

  cat >"$bin.tmp" <<EOF
#!/usr/bin/env python3
# explain-errors — instalado por install.sh (PREFIX=$PREFIX)
import sys
sys.path.insert(0, "$PREFIX/share/explain-errors")
from explain.cli import main
if __name__ == "__main__":
    main()
EOF
  mv "$bin.tmp" "$bin"
  chmod 755 "$bin"

  if [[ -d "$comps" ]]; then
    install -d "$dest/completions"
    install -m644 "$comps/explain.bash" "$dest/completions/"
    install -m644 "$comps/_explain" "$dest/completions/"
    install -m644 "$comps/explain.fish" "$dest/completions/"
  fi

  echo "Instalado explain-errors $ver"
  echo "  Lanzador:  $bin"
  echo "  Módulos:   $dest/explain/"
  echo "  Man page:  $man1"
  if [[ -d "$comps" ]]; then
    echo "  Completions: $dest/completions/  (bash, zsh, fish — ver README)"
  fi
  echo ""
  echo "Probar:    explain -h    |    man explain"
  if command -v mandb >/dev/null 2>&1; then
    echo "Opcional:  sudo mandb -q  (actualizar caché de man)"
  fi
}

do_uninstall() {
  local dest="$PREFIX/share/explain-errors"
  local bin="$PREFIX/bin/explain"
  local man1="$PREFIX/share/man/man1/explain.1"

  if [[ -f "$bin" ]]; then
    if ! grep -q 'explain-errors — instalado por install.sh' "$bin" 2>/dev/null; then
      die "no borro $bin: no parece el lanzador de explain-errors (abortando)"
    fi
    rm -f "$bin"
  fi

  rm -f "$man1"
  if [[ -d "$dest" ]]; then
    rm -rf "${dest:?}"
  fi
  # Si copiaste completions a sitios del sistema, borralos a mano (no asumimos esos paths)

  echo "Desinstalado (PREFIX=$PREFIX)."
}

ACTION="install"
while [[ $# -gt 0 ]]; do
  case "$1" in
    install) ACTION=install; shift ;;
    uninstall) ACTION=uninstall; shift ;;
    --prefix)
      PREFIX="${2:?}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "argumento desconocido: $1 (usá --help)"
      ;;
  esac
done

case "$ACTION" in
  install) do_install ;;
  uninstall) do_uninstall ;;
  *) die "acción inválida: $ACTION" ;;
esac
