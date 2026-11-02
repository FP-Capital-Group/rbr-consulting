#!/bin/bash
D="~/Desktop/AI/RBR AI/consegne/2026-10-09/img/originali"
osascript -e "set f to open for access POSIX file \"$D/$1.png\" with write permission" -e 'set eof f to 0' -e 'write (the clipboard as «class PNGf») to f' -e 'close access f' && ls -la "$D/$1.png" | awk '{print $5, $9}'

