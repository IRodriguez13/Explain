# fish completions for explain-errors
# Instalación: cp explain.fish ~/.config/fish/completions/explain.fish

complete -c explain -s h -l help -d 'Mostrar ayuda'
complete -c explain -l version -d 'Mostrar versión'

complete -c explain -s l -l lang -x -a 'auto C C++ Assembly C# Python JavaScript Rust' -d 'Lenguaje de la base de patrones'

complete -c explain -s v -l verbose -d 'Volcar log crudo en stderr antes del resumen'
complete -c explain -l full -d 'Formato extendido (separadores, bloques largos)'
complete -c explain -l ub-hints -d 'C/C++/Assembly: sección UB-RISK si hay -Wall/-fsanitize/… en cmd o salida'
complete -c explain -s nw -l no-warnings -d 'No mostrar advertencias ni listado de warnings'
complete -c explain -l max-warnings -x -a '1 3 5 10 20 50 100' -d 'Máx. advertencias sin patrón (sección feedback)'

complete -c explain -s m -l match -d 'Filtrar bloques por subcadena (mensaje, archivo, título, símbolo)' -r -f
complete -c explain -l shell -d 'Ejecutar CMD con shell del sistema (captura stdout+stderr)' -r
# fish no admite short multi-carácter; bash/zsh sí tienen -cnt
complete -c explain -l count -d 'Solo conteos (-cnt en bash/zsh; respeta -m, -nw, --ub-hints)'
complete -c explain -s f -s F -l man -x -a 'E1 W1 UB1 E2 W2 UB2' -d 'Ficha(s) didáctica(s); E1-2 W3 UB1…'
complete -c explain -l man-all -d 'Fichas con cápsula para todo E/W/UB que aplique'
complete -c explain -s i -l input-file -d 'Log compilador desde archivo (UTF-8)' -r -f
complete -c explain -l install-shell-completions -d 'Copiar completions a ~/.local, ~/.zsh, ~/.config/fish (Unix)'
