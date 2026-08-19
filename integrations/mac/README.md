# Puente Mac, Atajos e iPhone

El VPS no envía iMessage directamente. Kika publica una alerta por el túnel SSH reverso hacia una Mac autorizada; la Mac entrega el texto al Atajo `Kika Message`, y el Atajo envía el iMessage al destinatario definido por el propietario.

No se guarda un número telefónico, clave ni identificador personal en este repositorio. El destinatario se configura únicamente dentro del Atajo de macOS/iOS. El puerto del puente debe permanecer restringido a loopback y enlazado por SSH.
