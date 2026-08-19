# Dependencias y procedencia

Kika utiliza binarios locales `kika-ai`, `engram`, `pi`, `gga` y `opencode`. Las skills externas se mantienen instaladas bajo el perfil del usuario y se preservan como referencias en `skills/installed/`.

El repositorio upstream de habilidades es `Gentleman-Programming/Gentleman-Skills`; es una dependencia externa y no se copia completo aquí. La configuración funcional de Kika no depende de clonar ese repositorio en tiempo de ejecución.

Nunca se versionan credenciales, tokens, bases de datos de Engram, colas de runtime ni registros de operación.
