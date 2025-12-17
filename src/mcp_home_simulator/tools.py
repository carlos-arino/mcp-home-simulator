"""Definición de tools MCP y sus implementaciones."""

from typing import Dict, Any, Callable
from .state import HomeState


class MCPTools:
    """Define y mapea las tools MCP disponibles."""

    def __init__(self, state: HomeState):
        """
        Inicializa las tools MCP.

        Args:
            state: Instancia del estado del sistema.
        """
        self.state = state
        self._tools_registry: Dict[str, Callable] = {
            'get_presence': self.get_presence,
            'get_alarm_status': self.get_alarm_status,
            'list_lights_on': self.list_lights_on,
            'set_light_state': self.set_light_state,
            'set_alarm_state': self.set_alarm_state,
            'get_all_states': self.get_all_states,
        }

    def get_tool_definitions(self) -> Dict[str, Any]:
        """
        Obtiene las definiciones de todas las tools disponibles.

        Returns:
            Diccionario con las definiciones de tools en formato MCP.
        """
        return {
            'get_presence': {
                'name': 'get_presence',
                'description': 'Obtiene el estado del detector de presencia (quién está en casa)',
                'input_schema': {
                    'type': 'object',
                    'properties': {},
                    'required': []
                },
                'output_schema': {
                    'type': 'object',
                    'properties': {
                        'present': {'type': 'boolean'},
                        'known_people': {
                            'type': 'array',
                            'items': {'type': 'string'}
                        }
                    }
                }
            },
            'get_alarm_status': {
                'name': 'get_alarm_status',
                'description': 'Obtiene el estado actual de la alarma',
                'input_schema': {
                    'type': 'object',
                    'properties': {},
                    'required': []
                },
                'output_schema': {
                    'type': 'object',
                    'properties': {
                        'armed': {'type': 'boolean'}
                    }
                }
            },
            'list_lights_on': {
                'name': 'list_lights_on',
                'description': 'Lista todas las luces que están encendidas',
                'input_schema': {
                    'type': 'object',
                    'properties': {},
                    'required': []
                },
                'output_schema': {
                    'type': 'object',
                    'properties': {
                        'on': {
                            'type': 'array',
                            'items': {'type': 'string'}
                        }
                    }
                }
            },
            'set_light_state': {
                'name': 'set_light_state',
                'description': 'Enciende o apaga una luz específica',
                'input_schema': {
                    'type': 'object',
                    'properties': {
                        'name': {
                            'type': 'string',
                            'description': 'Nombre de la luz'
                        },
                        'on': {
                            'type': 'boolean',
                            'description': 'true para encender, false para apagar'
                        }
                    },
                    'required': ['name', 'on']
                },
                'output_schema': {
                    'type': 'object',
                    'properties': {
                        'ok': {'type': 'boolean'},
                        'error': {'type': 'string'}
                    }
                }
            },
            'set_alarm_state': {
                'name': 'set_alarm_state',
                'description': 'Arma o desarma la alarma',
                'input_schema': {
                    'type': 'object',
                    'properties': {
                        'armed': {
                            'type': 'boolean',
                            'description': 'true para armar, false para desarmar'
                        }
                    },
                    'required': ['armed']
                },
                'output_schema': {
                    'type': 'object',
                    'properties': {
                        'ok': {'type': 'boolean'}
                    }
                }
            },
            'get_all_states': {
                'name': 'get_all_states',
                'description': 'Obtiene un snapshot completo del estado del sistema',
                'input_schema': {
                    'type': 'object',
                    'properties': {},
                    'required': []
                },
                'output_schema': {
                    'type': 'object',
                    'properties': {
                        'lights': {
                            'type': 'object',
                            'additionalProperties': {'type': 'boolean'}
                        },
                        'alarm': {'type': 'boolean'},
                        'presence': {
                            'type': 'object',
                            'properties': {
                                'present': {'type': 'boolean'},
                                'known_people': {
                                    'type': 'array',
                                    'items': {'type': 'string'}
                                }
                            }
                        }
                    }
                }
            }
        }

    def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta una tool MCP.

        Args:
            tool_name: Nombre de la tool a ejecutar.
            args: Argumentos para la tool.

        Returns:
            Resultado de la ejecución de la tool.
        """
        if tool_name not in self._tools_registry:
            return {
                'ok': False,
                'error': f"Tool '{tool_name}' no encontrada"
            }

        try:
            handler = self._tools_registry[tool_name]
            return handler(args)
        except Exception as e:
            return {
                'ok': False,
                'error': f"Error al ejecutar tool: {str(e)}"
            }

    # ==================== IMPLEMENTACIONES DE TOOLS ====================

    def get_presence(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Implementa la tool get_presence."""
        return self.state.get_presence()

    def get_alarm_status(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Implementa la tool get_alarm_status."""
        return {'armed': self.state.get_alarm_status()}

    def list_lights_on(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Implementa la tool list_lights_on."""
        return {'on': self.state.list_lights_on()}

    def set_light_state(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Implementa la tool set_light_state."""
        name = args.get('name')
        on = args.get('on')

        if name is None or on is None:
            return {
                'ok': False,
                'error': 'Faltan parámetros requeridos: name, on'
            }

        success = self.state.set_light_state(name, on)
        if not success:
            return {
                'ok': False,
                'error': f"Luz '{name}' no encontrada"
            }

        return {'ok': True}

    def set_alarm_state(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Implementa la tool set_alarm_state."""
        armed = args.get('armed')

        if armed is None:
            return {
                'ok': False,
                'error': 'Falta parámetro requerido: armed'
            }

        self.state.set_alarm_state(armed)
        return {'ok': True}

    def get_all_states(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Implementa la tool get_all_states."""
        return self.state.get_all_states()
