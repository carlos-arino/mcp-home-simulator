"""Servidor MCP por stdio - Protocolo simplificado JSON line-delimited."""

import sys
import json
from typing import Dict, Any, Optional
from .tools import MCPTools
from .state import HomeState
from .config import Config


class MCPStdioServer:
    """Servidor MCP que comunica por stdin/stdout usando JSON line-delimited."""

    def __init__(self, config_path: str = "config.yaml"):
        """
        Inicializa el servidor MCP.

        Args:
            config_path: Ruta al archivo de configuración.
        """
        self.config = Config(config_path)
        self.state = HomeState(self.config)
        self.tools = MCPTools(self.state)
        self.running = False

    def send_message(self, message: Dict[str, Any]) -> None:
        """
        Envía un mensaje JSON por stdout.

        Args:
            message: Diccionario con el mensaje a enviar.
        """
        json_str = json.dumps(message, ensure_ascii=False)
        print(json_str, flush=True)

    def send_ready(self) -> None:
        """Envía el mensaje de handshake inicial con las tools disponibles."""
        tools_definitions = self.tools.get_tool_definitions()

        message = {
            'type': 'ready',
            'version': '0.1.0',
            'tools': list(tools_definitions.values())
        }

        self.send_message(message)

    def handle_call(self, message: Dict[str, Any]) -> None:
        """
        Procesa una llamada a una tool MCP.

        Args:
            message: Mensaje con la llamada a procesar.
        """
        msg_id = message.get('id')
        tool_name = message.get('tool')
        args = message.get('args', {})

        if not msg_id or not tool_name:
            self.send_error(msg_id, "Mensaje inválido: falta 'id' o 'tool'")
            return

        # Ejecutar la tool
        result = self.tools.execute_tool(tool_name, args)

        # Verificar si hubo error
        if isinstance(result, dict) and result.get('ok') is False:
            self.send_error(msg_id, result.get('error', 'Error desconocido'))
        else:
            self.send_result(msg_id, result)

    def send_result(self, msg_id: Any, result: Any) -> None:
        """
        Envía un mensaje de resultado exitoso.

        Args:
            msg_id: ID del mensaje original.
            result: Resultado de la operación.
        """
        message = {
            'type': 'result',
            'id': msg_id,
            'ok': True,
            'result': result
        }
        self.send_message(message)

    def send_error(self, msg_id: Optional[Any], error: str) -> None:
        """
        Envía un mensaje de error.

        Args:
            msg_id: ID del mensaje original (puede ser None).
            error: Descripción del error.
        """
        message = {
            'type': 'error',
            'id': msg_id,
            'ok': False,
            'error': error
        }
        self.send_message(message)

    def process_message(self, line: str) -> None:
        """
        Procesa una línea de entrada JSON.

        Args:
            line: Línea JSON a procesar.
        """
        try:
            message = json.loads(line)
        except json.JSONDecodeError as e:
            self.send_error(None, f"Error al parsear JSON: {e}")
            return

        msg_type = message.get('type')

        if msg_type == 'call':
            self.handle_call(message)
        elif msg_type == 'quit':
            self.running = False
        else:
            self.send_error(message.get('id'),
                            f"Tipo de mensaje desconocido: {msg_type}")

    def run(self) -> None:
        """
        Ejecuta el bucle principal del servidor MCP.

        Lee líneas de stdin, procesa mensajes y responde por stdout.
        """
        # Enviar mensaje de handshake
        self.send_ready()

        # Bucle principal
        self.running = True
        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue

                self.process_message(line)

                if not self.running:
                    break
        except KeyboardInterrupt:
            pass
        except Exception as e:
            self.send_error(None, f"Error interno del servidor: {e}")


def start_mcp_server(config_path: str = "config.yaml") -> None:
    """
    Inicia el servidor MCP por stdio.

    Args:
        config_path: Ruta al archivo de configuración.
    """
    server = MCPStdioServer(config_path)
    server.run()
