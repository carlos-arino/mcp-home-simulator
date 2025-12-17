"""Punto de entrada principal para el simulador de domótica."""

import sys
import argparse
from typing import Optional, List
from .cli import run_cli
from .mcp_stdio import start_mcp_server


def main(argv: Optional[List[str]] = None) -> int:
    """
    Punto de entrada principal de la aplicación.

    Determina si debe ejecutarse en modo MCP (stdio) o modo CLI.

    Args:
        argv: Argumentos de línea de comandos (None = usar sys.argv).

    Returns:
        Código de salida.
    """
    if argv is None:
        argv = sys.argv[1:]

    # Verificar si se solicita modo MCP
    if '--mcp' in argv or '--mcp=stdio' in argv:
        # Modo MCP stdio
        config_path = 'config.yaml'

        # Extraer config si está especificado
        for i, arg in enumerate(argv):
            if arg.startswith('--config='):
                config_path = arg.split('=', 1)[1]
            elif arg == '--config' and i + 1 < len(argv):
                config_path = argv[i + 1]

        start_mcp_server(config_path)
        return 0
    else:
        # Modo CLI
        return run_cli(argv)


if __name__ == '__main__':
    sys.exit(main())
