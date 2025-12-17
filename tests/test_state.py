"""Tests para el módulo de estado (state.py)."""

import pytest
from mcp_home_simulator.config import Config
from mcp_home_simulator.state import HomeState


class TestHomeState:
    """Tests para la clase HomeState."""

    @pytest.fixture
    def mock_config(self):
        """Crea una configuración mock para tests."""
        config = Config.__new__(Config)
        config.data = {
            'lights': ['salon', 'cocina', 'dormitorio'],
            'alarm_default': False,
            'presence_default': {'present': False, 'known_people': []}
        }
        return config

    @pytest.fixture
    def state(self, mock_config):
        """Crea una instancia de HomeState para tests."""
        return HomeState(mock_config)

    # ==================== Tests de Luces ====================

    def test_initial_lights_state(self, state):
        """Verifica que las luces inician apagadas."""
        assert state.lights == {
            'salon': False,
            'cocina': False,
            'dormitorio': False
        }

    def test_get_light_state_existing(self, state):
        """Verifica obtener estado de luz existente."""
        assert state.get_light_state('salon') is False

    def test_get_light_state_non_existing(self, state):
        """Verifica obtener estado de luz inexistente."""
        assert state.get_light_state('inexistente') is None

    def test_set_light_state_on(self, state):
        """Verifica encender una luz."""
        result = state.set_light_state('salon', True)
        assert result is True
        assert state.get_light_state('salon') is True

    def test_set_light_state_off(self, state):
        """Verifica apagar una luz."""
        state.set_light_state('salon', True)
        result = state.set_light_state('salon', False)
        assert result is True
        assert state.get_light_state('salon') is False

    def test_set_light_state_non_existing(self, state):
        """Verifica intentar cambiar luz inexistente."""
        result = state.set_light_state('inexistente', True)
        assert result is False

    def test_list_lights_on_empty(self, state):
        """Verifica listar luces encendidas cuando no hay ninguna."""
        assert state.list_lights_on() == []

    def test_list_lights_on_multiple(self, state):
        """Verifica listar múltiples luces encendidas."""
        state.set_light_state('salon', True)
        state.set_light_state('cocina', True)
        lights_on = state.list_lights_on()
        assert set(lights_on) == {'salon', 'cocina'}

    def test_get_all_lights(self, state):
        """Verifica obtener todas las luces."""
        state.set_light_state('salon', True)
        all_lights = state.get_all_lights()
        assert all_lights == {
            'salon': True,
            'cocina': False,
            'dormitorio': False
        }

    # ==================== Tests de Alarma ====================

    def test_initial_alarm_state(self, state):
        """Verifica estado inicial de alarma."""
        assert state.get_alarm_status() is False

    def test_set_alarm_armed(self, state):
        """Verifica armar alarma."""
        result = state.set_alarm_state(True)
        assert result is True
        assert state.get_alarm_status() is True

    def test_set_alarm_disarmed(self, state):
        """Verifica desarmar alarma."""
        state.set_alarm_state(True)
        result = state.set_alarm_state(False)
        assert result is True
        assert state.get_alarm_status() is False

    # ==================== Tests de Presencia ====================

    def test_initial_presence_state(self, state):
        """Verifica estado inicial de presencia."""
        presence = state.get_presence()
        assert presence == {
            'present': False,
            'known_people': []
        }

    def test_set_presence_single_person(self, state):
        """Verifica establecer una persona presente."""
        result = state.set_presence(['Carlos'])
        assert result is True
        presence = state.get_presence()
        assert presence['present'] is True
        assert presence['known_people'] == ['Carlos']

    def test_set_presence_multiple_people(self, state):
        """Verifica establecer múltiples personas."""
        result = state.set_presence(['Carlos', 'Ana'])
        assert result is True
        presence = state.get_presence()
        assert presence['present'] is True
        assert set(presence['known_people']) == {'Carlos', 'Ana'}

    def test_set_presence_empty_list(self, state):
        """Verifica establecer lista vacía de personas."""
        state.set_presence(['Carlos'])
        result = state.set_presence([])
        assert result is True
        presence = state.get_presence()
        assert presence['present'] is False
        assert presence['known_people'] == []

    def test_add_person(self, state):
        """Verifica añadir persona."""
        result = state.add_person('Carlos')
        assert result is True
        presence = state.get_presence()
        assert 'Carlos' in presence['known_people']
        assert presence['present'] is True

    def test_add_person_duplicate(self, state):
        """Verifica añadir persona duplicada."""
        state.add_person('Carlos')
        state.add_person('Carlos')
        presence = state.get_presence()
        assert presence['known_people'].count('Carlos') == 1

    def test_remove_person_existing(self, state):
        """Verifica eliminar persona existente."""
        state.set_presence(['Carlos', 'Ana'])
        result = state.remove_person('Carlos')
        assert result is True
        presence = state.get_presence()
        assert 'Carlos' not in presence['known_people']
        assert 'Ana' in presence['known_people']
        assert presence['present'] is True

    def test_remove_person_non_existing(self, state):
        """Verifica eliminar persona inexistente."""
        result = state.remove_person('Inexistente')
        assert result is False

    def test_remove_last_person(self, state):
        """Verifica que present=False al eliminar última persona."""
        state.set_presence(['Carlos'])
        state.remove_person('Carlos')
        presence = state.get_presence()
        assert presence['present'] is False
        assert presence['known_people'] == []

    def test_clear_presence(self, state):
        """Verifica limpiar presencia."""
        state.set_presence(['Carlos', 'Ana'])
        result = state.clear_presence()
        assert result is True
        presence = state.get_presence()
        assert presence['present'] is False
        assert presence['known_people'] == []

    # ==================== Tests de Estado General ====================

    def test_get_all_states(self, state):
        """Verifica obtener snapshot completo."""
        state.set_light_state('salon', True)
        state.set_alarm_state(True)
        state.set_presence(['Carlos'])

        all_states = state.get_all_states()

        assert 'lights' in all_states
        assert 'alarm' in all_states
        assert 'presence' in all_states

        assert all_states['lights']['salon'] is True
        assert all_states['alarm'] is True
        assert all_states['presence']['present'] is True
        assert 'Carlos' in all_states['presence']['known_people']
