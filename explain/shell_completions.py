"""Instalar scripts de Tab completion (bash/zsh/fish) en el home del usuario."""

from __future__ import annotations

import os
import shutil
import sys
import sysconfig
from pathlib import Path


def _completions_source_dir() -> Path:
    """Directorio que contiene explain.bash, _explain, explain.fish."""
    # Repo clonado o editable: explain/shell_completions.py → raíz del repo
    here = Path(__file__).resolve()
    repo_root = here.parent.parent
    cand = repo_root / "completions"
    if (cand / "explain.bash").is_file():
        return cand
    # pip install (wheel/sdist): datos en PREFIX/share/explain-errors/completions
    try:
        data = Path(sysconfig.get_path("data"))
    except Exception:
        data = Path()
    installed = data / "share" / "explain-errors" / "completions"
    if (installed / "explain.bash").is_file():
        return installed
    raise FileNotFoundError(
        "No se encontraron completions (explain.bash). "
        "Instalá el paquete con pip o usá un clone completo del repo."
    )


def install_shell_completions(*, verbose: bool = True) -> int:
    """
    Copia bash/zsh/fish a las rutas habituales bajo $HOME.
    Solo Unix; en Windows imprime aviso y retorna 0.
    """
    if os.name == "nt":
        if verbose:
            print(
                "(explain) La instalación de completions de shell es solo para Unix "
                "(bash/zsh/fish). En Windows/WSL usá Git Bash o WSL.",
                file=sys.stderr,
            )
        return 0

    try:
        src = _completions_source_dir()
    except FileNotFoundError as e:
        print(f"explain: {e}", file=sys.stderr)
        return 1

    home = Path.home()
    done: list[str] = []

    bash_dir = home / ".local" / "share" / "bash-completion" / "completions"
    bash_dir.mkdir(parents=True, mode=0o755, exist_ok=True)
    bash_dest = bash_dir / "explain"
    shutil.copy2(src / "explain.bash", bash_dest)
    bash_dest.chmod(0o644)
    done.append(str(bash_dest))

    zsh_dir = home / ".zsh" / "completions"
    zsh_dir.mkdir(parents=True, mode=0o755, exist_ok=True)
    zsh_dest = zsh_dir / "_explain"
    shutil.copy2(src / "_explain", zsh_dest)
    zsh_dest.chmod(0o644)
    done.append(str(zsh_dest))

    fish_dir = home / ".config" / "fish" / "completions"
    fish_dir.mkdir(parents=True, mode=0o755, exist_ok=True)
    fish_dest = fish_dir / "explain.fish"
    shutil.copy2(src / "explain.fish", fish_dest)
    fish_dest.chmod(0o644)
    done.append(str(fish_dest))

    if verbose:
        print("(explain · instalación de completions)")
        for p in done:
            print(f"  → {p}")
        print("")
        print("Bash: abrí una terminal nueva o ejecutá:")
        print(f"  source {bash_dest}")
        print("Zsh: asegurate de tener en ~/.zshrc algo como:")
        print("  fpath+=(~/.zsh/completions) && autoload -Uz compinit && compinit")
        print("Fish: no requiere pasos extra si ~/.config/fish/completions existe.")
    return 0
