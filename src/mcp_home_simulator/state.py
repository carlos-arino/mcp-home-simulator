"""Módulo de estado para el simulador de domótica."""

from typing import Dict, List, Optional, Any
from .config import Config


class HomeState:
    """Gestiona el estado en memoria del sistema de domótica."""

    def __init__(self, config: Config):
        """
        Inicializa el estado del sistema.

        Args:
            config: Objeto de configuración.
        """
        self.config = config

        # Estado de las luces: {nombre: encendida}
        self.lights: Dict[str, bool] = {
            light: False for light in config.lights}

        # Estado de la alarma
        self.alarm_armed: bool = config.alarm_default

        # Estado de presencia
        self.presence: Dict[str, Any] = {
            'present': config.presence_default['present'],
            'known_people': list(config.presence_default['known_people'])
        }

    # ==================== LUCES ====================

    def get_light_state(self, name: str) -> Optional[bool]:
        """
        Obtiene el estado de una luz.

        Args:
            name: Nombre de la luz.

        Returns:
            True si está encendida, False si está apagada, None si no existe.
        """
        return self.lights.get(name)

    def set_light_state(self, name: str, on: bool) -> bool:
        """
        Cambia el estado de una luz.

        Args:
            name: Nombre de la luz.
            on: True para encender, False para apagar.

        Returns:
            True si la operación fue exitosa, False si la luz no existe.
        """
        if name not in self.lights:
            return False

        self.lights[name] = on
        return True

    def list_lights_on(self) -> List[str]:
        """
        Obtiene la lista de luces encendidas.

        Returns:
            Lista con nombres de luces encendidas.
        """
        return [name for name, state in self.lights.items() if state]

    def get_all_lights(self) -> Dict[str, bool]:
        """
        Obtiene el estado de todas las luces.

        Returns:
            Diccionario con todas las luces y sus estados.
        """
        return dict(self.lights)

    # ==================== ALARMA ====================

    def get_alarm_status(self) -> bool:
        """
        Obtiene el estado de la alarma.

        Returns:
            True si está armada, False si está desarmada.
        """
        return self.alarm_armed

    def set_alarm_state(self, armed: bool) -> bool:
        """
        Cambia el estado de la alarma.

        Args:
            armed: True para armar, False para desarmar.

        Returns:
            True (siempre exitoso).
        """
        self.alarm_armed = armed
        return True

    # ==================== PRESENCIA ====================

    def get_presence(self) -> Dict[str, Any]:
        """
        Obtiene el estado del detector de presencia.

        Returns:
            Diccionario con 'present' (bool) y 'known_people' (list).
        """
        return {
            'present': self.presence['present'],
            'known_people': list(self.presence['known_people'])
        }

    def set_presence(self, people: List[str]) -> bool:
        """
        Establece las personas presentes.

        Args:
            people: Lista de nombres de personas presentes.

        Returns:
            True (siempre exitoso).
        """
        self.presence['known_people'] = list(people)
        self.presence['present'] = len(people) > 0
        return True

    def add_person(self, name: str) -> bool:
        """
        Añade una persona a la lista de presentes.

        Args:
            name: Nombre de la persona.

        Returns:
            True (siempre exitoso).
        """
        if name not in self.presence['known_people']:
            self.presence['known_people'].append(name)
        self.presence['present'] = True
        return True

    def remove_person(self, name: str) -> bool:
        """
        Elimina una persona de la lista de presentes.

        Args:
            name: Nombre de la persona.

        Returns:
            True si se eliminó, False si no estaba en la lista.
        """
        if name in self.presence['known_people']:
            self.presence['known_people'].remove(name)
            self.presence['present'] = len(self.presence['known_people']) > 0
            return True
        return False

    def clear_presence(self) -> bool:
        """
        Limpia la lista de personas presentes.

        Returns:
            True (siempre exitoso).
        """
        self.presence['known_people'] = []
        self.presence['present'] = False
        return True

    # ==================== ESTADO GENERAL ====================

    def get_all_states(self) -> Dict[str, Any]:
        """
        Obtiene un snapshot completo del estado del sistema.

        Returns:
            Diccionario con lights, alarm y presence.
        """
        return {
            'lights': self.get_all_lights(),
            'alarm': self.alarm_armed,
            'presence': self.get_presence()
        }
