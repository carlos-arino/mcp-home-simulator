"""Tests para el servidor MCP (mcp_stdio.py)."""

import pytest
import json
from io import StringIO
from mcp_home_simulator.mcp_stdio import MCPStdioServer
from mcp_home_simulator.config import Config


class TestMCPStdioServer:
    """Tests para el servidor MCP."""

    @pytest.fixture
    def mock_config(self):
        """Crea una configuración mock para tests."""
        config = Config.__new__(Config)
        config.data = {
            'lights': ['salon', 'cocina'],
            'alarm_default': False,
            'presence_default': {'present': False, 'known_people': []}
        }
        return config

    @pytest.fixture
    def server(self, mock_config, monkeypatch):
        """Crea un servidor MCP para tests."""

        def mock_config_init(self, config_path="config.yaml"):
            self.config_path = config_path
            self.data = mock_config.data

        monkeypatch.setattr(Config, '__init__', mock_config_init)
        return MCPStdioServer()

    # ==================== Tests de Mensajes ====================

    def test_send_ready(self, server, capsys):
        """Verifica envío de mensaje ready."""
        server.send_ready()
        captured = capsys.readouterr()

        message = json.loads(captured.out.strip())
        assert message['type'] == 'ready'
        assert 'version' in message
        assert 'tools' in message
        assert len(message['tools']) > 0

    def test_send_result(self, server, capsys):
        """Verifica envío de mensaje result."""
        server.send_result(1, {'ok': True})
        captured = capsys.readouterr()

        message = json.loads(captured.out.strip())
        assert message['type'] == 'result'
        assert message['id'] == 1
        assert message['ok'] is True
        assert message['result'] == {'ok': True}

    def test_send_error(self, server, capsys):
        """Verifica envío de mensaje error."""
        server.send_error(1, 'Test error')
        captured = capsys.readouterr()

        message = json.loads(captured.out.strip())
        assert message['type'] == 'error'
        assert message['id'] == 1
        assert message['ok'] is False
        assert message['error'] == 'Test error'

    # ==================== Tests de Procesamiento ====================

    def test_handle_call_get_presence(self, server, capsys):
        """Verifica manejo de llamada get_presence."""
        message = {
            'type': 'call',
            'id': 1,
            'tool': 'get_presence',
            'args': {}
        }

        server.handle_call(message)
        captured = capsys.readouterr()

        response = json.loads(captured.out.strip())
        assert response['type'] == 'result'
        assert response['id'] == 1
        assert 'result' in response
        assert 'present' in response['result']
        assert 'known_people' in response['result']

    def test_handle_call_get_alarm_status(self, server, capsys):
        """Verifica manejo de llamada get_alarm_status."""
        message = {
            'type': 'call',
            'id': 2,
            'tool': 'get_alarm_status',
            'args': {}
        }

        server.handle_call(message)
        captured = capsys.readouterr()

        response = json.loads(captured.out.strip())
        assert response['type'] == 'result'
        assert 'armed' in response['result']

    def test_handle_call_list_lights_on(self, server, capsys):
        """Verifica manejo de llamada list_lights_on."""
        server.state.set_light_state('salon', True)

        message = {
            'type': 'call',
            'id': 3,
            'tool': 'list_lights_on',
            'args': {}
        }

        server.handle_call(message)
        captured = capsys.readouterr()

        response = json.loads(captured.out.strip())
        assert response['type'] == 'result'
        assert 'on' in response['result']
        assert 'salon' in response['result']['on']

    def test_handle_call_set_light_state_success(self, server, capsys):
        """Verifica manejo exitoso de set_light_state."""
        message = {
            'type': 'call',
            'id': 4,
            'tool': 'set_light_state',
            'args': {'name': 'salon', 'on': True}
        }

        server.handle_call(message)
        captured = capsys.readouterr()

        response = json.loads(captured.out.strip())
        assert response['type'] == 'result'
        assert response['result']['ok'] is True
        assert server.state.get_light_state('salon') is True

    def test_handle_call_set_light_state_not_found(self, server, capsys):
        """Verifica error al establecer luz inexistente."""
        message = {
            'type': 'call',
            'id': 5,
            'tool': 'set_light_state',
            'args': {'name': 'inexistente', 'on': True}
        }

        server.handle_call(message)
        captured = capsys.readouterr()

        response = json.loads(captured.out.strip())
        assert response['type'] == 'error'
        assert response['ok'] is False
        assert 'error' in response

    def test_handle_call_set_alarm_state(self, server, capsys):
        """Verifica manejo de set_alarm_state."""
        message = {
            'type': 'call',
            'id': 6,
            'tool': 'set_alarm_state',
            'args': {'armed': True}
        }

        server.handle_call(message)
        captured = capsys.readouterr()

        response = json.loads(captured.out.strip())
        assert response['type'] == 'result'
        assert response['result']['ok'] is True
        assert server.state.get_alarm_status() is True

    def test_handle_call_get_all_states(self, server, capsys):
        """Verifica manejo de get_all_states."""
        server.state.set_light_state('salon', True)
        server.state.set_alarm_state(True)
        server.state.set_presence(['Carlos'])

        message = {
            'type': 'call',
            'id': 7,
            'tool': 'get_all_states',
            'args': {}
        }

        server.handle_call(message)
        captured = capsys.readouterr()

        response = json.loads(captured.out.strip())
        assert response['type'] == 'result'
        assert 'lights' in response['result']
        assert 'alarm' in response['result']
        assert 'presence' in response['result']
        assert response['result']['lights']['salon'] is True
        assert response['result']['alarm'] is True
        assert 'Carlos' in response['result']['presence']['known_people']

    def test_handle_call_unknown_tool(self, server, capsys):
        """Verifica error con tool desconocida."""
        message = {
            'type': 'call',
            'id': 8,
            'tool': 'unknown_tool',
            'args': {}
        }

        server.handle_call(message)
        captured = capsys.readouterr()

        response = json.loads(captured.out.strip())
        assert response['type'] == 'error'
        assert 'no encontrada' in response['error']

    def test_handle_call_missing_id(self, server, capsys):
        """Verifica error con mensaje sin ID."""
        message = {
            'type': 'call',
            'tool': 'get_presence',
            'args': {}
        }

        server.handle_call(message)
        captured = capsys.readouterr()

        response = json.loads(captured.out.strip())
        assert response['type'] == 'error'

    def test_process_message_invalid_json(self, server, capsys):
        """Verifica error con JSON inválido."""
        server.process_message('invalid json{')
        captured = capsys.readouterr()

        response = json.loads(captured.out.strip())
        assert response['type'] == 'error'
        assert 'parsear JSON' in response['error']

    def test_process_message_quit(self, server):
        """Verifica procesamiento de mensaje quit."""
        server.running = True
        message = json.dumps({'type': 'quit'})
        server.process_message(message)

        assert server.running is False
