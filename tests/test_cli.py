"""Tests para la interfaz CLI."""

import pytest
from io import StringIO
import sys
from mcp_home_simulator.cli import CLI, create_parser, run_cli
from mcp_home_simulator.config import Config
from argparse import Namespace


class TestCLI:
    """Tests para la interfaz CLI."""

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
    def cli(self, mock_config, monkeypatch):
        """Crea una instancia de CLI para tests."""
        # Mock Config para que no intente cargar archivo real

        def mock_init(self, config_path="config.yaml"):
            self.config = mock_config
            from mcp_home_simulator.state import HomeState
            self.state = HomeState(self.config)

        monkeypatch.setattr(CLI, '__init__', mock_init)
        return CLI()

    # ==================== Tests de Comandos ====================

    def test_cmd_status(self, cli, capsys):
        """Verifica comando status."""
        args = Namespace()
        result = cli.cmd_status(args)

        assert result == 0
        captured = capsys.readouterr()
        assert 'ESTADO GENERAL' in captured.out
        assert 'LUCES' in captured.out
        assert 'ALARMA' in captured.out
        assert 'PRESENCIA' in captured.out

    def test_cmd_lights_list(self, cli, capsys):
        """Verifica comando lights list."""
        cli.state.set_light_state('salon', True)
        args = Namespace()
        result = cli.cmd_lights_list(args)

        assert result == 0
        captured = capsys.readouterr()
        assert 'salon' in captured.out
        assert 'cocina' in captured.out

    def test_cmd_lights_on_success(self, cli, capsys):
        """Verifica comando lights on exitoso."""
        args = Namespace(name='salon')
        result = cli.cmd_lights_on(args)

        assert result == 0
        assert cli.state.get_light_state('salon') is True
        captured = capsys.readouterr()
        assert 'encendida' in captured.out.lower()

    def test_cmd_lights_on_not_found(self, cli, capsys):
        """Verifica comando lights on con luz inexistente."""
        args = Namespace(name='inexistente')
        result = cli.cmd_lights_on(args)

        assert result == 1
        captured = capsys.readouterr()
        assert 'Error' in captured.out or 'error' in captured.out

    def test_cmd_lights_off_success(self, cli, capsys):
        """Verifica comando lights off exitoso."""
        cli.state.set_light_state('salon', True)
        args = Namespace(name='salon')
        result = cli.cmd_lights_off(args)

        assert result == 0
        assert cli.state.get_light_state('salon') is False
        captured = capsys.readouterr()
        assert 'apagada' in captured.out.lower()

    def test_cmd_alarm_on(self, cli, capsys):
        """Verifica comando alarm on."""
        args = Namespace()
        result = cli.cmd_alarm_on(args)

        assert result == 0
        assert cli.state.get_alarm_status() is True
        captured = capsys.readouterr()
        assert 'ARMADA' in captured.out

    def test_cmd_alarm_off(self, cli, capsys):
        """Verifica comando alarm off."""
        cli.state.set_alarm_state(True)
        args = Namespace()
        result = cli.cmd_alarm_off(args)

        assert result == 0
        assert cli.state.get_alarm_status() is False
        captured = capsys.readouterr()
        assert 'DESARMADA' in captured.out

    def test_cmd_presence_show(self, cli, capsys):
        """Verifica comando presence show."""
        cli.state.set_presence(['Carlos', 'Ana'])
        args = Namespace()
        result = cli.cmd_presence_show(args)

        assert result == 0
        captured = capsys.readouterr()
        assert 'Carlos' in captured.out
        assert 'Ana' in captured.out

    def test_cmd_presence_set(self, cli, capsys):
        """Verifica comando presence set."""
        args = Namespace(names=['Carlos', 'Ana'])
        result = cli.cmd_presence_set(args)

        assert result == 0
        presence = cli.state.get_presence()
        assert set(presence['known_people']) == {'Carlos', 'Ana'}
        assert presence['present'] is True

    def test_cmd_presence_clear(self, cli, capsys):
        """Verifica comando presence clear."""
        cli.state.set_presence(['Carlos'])
        args = Namespace()
        result = cli.cmd_presence_clear(args)

        assert result == 0
        presence = cli.state.get_presence()
        assert presence['present'] is False
        assert presence['known_people'] == []

    # ==================== Tests de Parser ====================

    def test_create_parser(self):
        """Verifica creación del parser."""
        parser = create_parser()
        assert parser is not None
        assert parser.prog == 'mcp-home-simulator'

    def test_parser_status_command(self):
        """Verifica parseo de comando status."""
        parser = create_parser()
        args = parser.parse_args(['status'])
        assert args.command == 'status'

    def test_parser_lights_on_command(self):
        """Verifica parseo de comando lights on."""
        parser = create_parser()
        args = parser.parse_args(['lights', 'on', 'salon'])
        assert args.command == 'lights'
        assert args.lights_command == 'on'
        assert args.name == 'salon'

    def test_parser_alarm_command(self):
        """Verifica parseo de comando alarm."""
        parser = create_parser()
        args = parser.parse_args(['alarm', 'on'])
        assert args.command == 'alarm'
        assert args.alarm_command == 'on'

    def test_parser_presence_set_command(self):
        """Verifica parseo de comando presence set."""
        parser = create_parser()
        args = parser.parse_args(['presence', 'set', 'Carlos', 'Ana'])
        assert args.command == 'presence'
        assert args.presence_command == 'set'
        assert args.names == ['Carlos', 'Ana']
