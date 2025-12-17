"""Módulo de configuración para el simulador de domótica."""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Any


DEFAULT_CONFIG = """lights:
  - salon
  - cocina
  - dormitorio
  - bano
  - garage

alarm_default: false

presence_default:
  present: false
  known_people: []
"""


class Config:
    """Maneja la configuración del simulador desde config.yaml."""

    def __init__(self, config_path: str = "config.yaml"):
        """
        Inicializa la configuración.

        Args:
            config_path: Ruta al archivo de configuración YAML.
        """
        self.config_path = Path(config_path)
        self.data = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Carga la configuración desde el archivo YAML.

        Si el archivo no existe, crea uno con valores predeterminados.

        Returns:
            Diccionario con la configuración cargada.
        """
        if not self.config_path.exists():
            print(
                f"⚠️  Archivo de configuración no encontrado. Creando {self.config_path}...")
            self._create_default_config()

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            # Validar configuración
            self._validate_config(config)
            return config
        except Exception as e:
            raise ValueError(f"Error al cargar configuración: {e}")

    def _create_default_config(self) -> None:
        """Crea un archivo de configuración predeterminado."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            f.write(DEFAULT_CONFIG)

    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        Valida la estructura de la configuración.

        Args:
            config: Diccionario de configuración a validar.

        Raises:
            ValueError: Si la configuración no es válida.
        """
        if not isinstance(config, dict):
            raise ValueError("La configuración debe ser un diccionario")

        if 'lights' not in config or not isinstance(config['lights'], list):
            raise ValueError("'lights' debe ser una lista")

        if not config['lights']:
            raise ValueError("Debe haber al menos una luz configurada")

        if 'alarm_default' not in config:
            config['alarm_default'] = False

        if 'presence_default' not in config:
            config['presence_default'] = {'present': False, 'known_people': []}

    @property
    def lights(self) -> List[str]:
        """Obtiene la lista de luces configuradas."""
        return self.data.get('lights', [])

    @property
    def alarm_default(self) -> bool:
        """Obtiene el estado predeterminado de la alarma."""
        return self.data.get('alarm_default', False)

    @property
    def presence_default(self) -> Dict[str, Any]:
        """Obtiene el estado predeterminado de presencia."""
        return self.data.get('presence_default', {'present': False, 'known_people': []})
