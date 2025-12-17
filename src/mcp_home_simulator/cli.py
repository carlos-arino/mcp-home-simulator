"""Interfaz CLI para el simulador de domótica."""

import argparse
import sys
from typing import List, Optional
from .config import Config
from .state import HomeState


class CLI:
    """Interfaz de línea de comandos para el simulador."""

    def __init__(self, config_path: str = "config.yaml"):
        """
        Inicializa la CLI.

        Args:
            config_path: Ruta al archivo de configuración.
        """
        self.config = Config(config_path)
        self.state = HomeState(self.config)

    def cmd_status(self, args: argparse.Namespace) -> int:
        """
        Muestra el estado general del sistema.

        Args:
            args: Argumentos parseados.

        Returns:
            Código de salida (0 = éxito).
        """
        state = self.state.get_all_states()

        print("╔═══════════════════════════════════════════╗")
        print("║    ESTADO GENERAL DEL SISTEMA DOMÓTICO   ║")
        print("╚═══════════════════════════════════════════╝")
        print()

        # Luces
        print("🔆 LUCES:")
        for name, is_on in state['lights'].items():
            status = "🟢 Encendida" if is_on else "⚫ Apagada"
            print(f"  • {name}: {status}")
        print()

        # Alarma
        alarm_status = "🔴 ARMADA" if state['alarm'] else "🟢 Desarmada"
        print(f"🚨 ALARMA: {alarm_status}")
        print()

        # Presencia
        presence = state['presence']
        present_status = "✅ Hay personas" if presence['present'] else "❌ No hay nadie"
        print(f"👥 PRESENCIA: {present_status}")
        if presence['known_people']:
            print(
                f"  Personas presentes: {', '.join(presence['known_people'])}")
        print()

        return 0

    def cmd_lights_list(self, args: argparse.Namespace) -> int:
        """
        Lista todas las luces y su estado.

        Args:
            args: Argumentos parseados.

        Returns:
            Código de salida.
        """
        lights = self.state.get_all_lights()

        print("🔆 ESTADO DE LAS LUCES:")
        for name, is_on in lights.items():
            status = "🟢 Encendida" if is_on else "⚫ Apagada"
            print(f"  • {name}: {status}")

        return 0

    def cmd_lights_on(self, args: argparse.Namespace) -> int:
        """
        Enciende una luz específica.

        Args:
            args: Argumentos parseados (debe contener 'name').

        Returns:
            Código de salida.
        """
        name = args.name
        success = self.state.set_light_state(name, True)

        if not success:
            print(f"❌ Error: La luz '{name}' no existe.")
            print(
                f"   Luces disponibles: {', '.join(self.state.lights.keys())}")
            return 1

        print(f"✅ Luz '{name}' encendida.")
        return 0

    def cmd_lights_off(self, args: argparse.Namespace) -> int:
        """
        Apaga una luz específica.

        Args:
            args: Argumentos parseados (debe contener 'name').

        Returns:
            Código de salida.
        """
        name = args.name
        success = self.state.set_light_state(name, False)

        if not success:
            print(f"❌ Error: La luz '{name}' no existe.")
            print(
                f"   Luces disponibles: {', '.join(self.state.lights.keys())}")
            return 1

        print(f"✅ Luz '{name}' apagada.")
        return 0

    def cmd_alarm_on(self, args: argparse.Namespace) -> int:
        """
        Arma la alarma.

        Args:
            args: Argumentos parseados.

        Returns:
            Código de salida.
        """
        self.state.set_alarm_state(True)
        print("🚨 Alarma ARMADA.")
        return 0

    def cmd_alarm_off(self, args: argparse.Namespace) -> int:
        """
        Desarma la alarma.

        Args:
            args: Argumentos parseados.

        Returns:
            Código de salida.
        """
        self.state.set_alarm_state(False)
        print("✅ Alarma DESARMADA.")
        return 0

    def cmd_presence_show(self, args: argparse.Namespace) -> int:
        """
        Muestra el estado de presencia.

        Args:
            args: Argumentos parseados.

        Returns:
            Código de salida.
        """
        presence = self.state.get_presence()

        print("👥 DETECTOR DE PRESENCIA:")
        status = "✅ Hay personas en casa" if presence['present'] else "❌ No hay nadie en casa"
        print(f"  Estado: {status}")

        if presence['known_people']:
            print(f"  Personas presentes:")
            for person in presence['known_people']:
                print(f"    • {person}")
        else:
            print(f"  Personas presentes: (ninguna)")

        return 0

    def cmd_presence_set(self, args: argparse.Namespace) -> int:
        """
        Establece las personas presentes.

        Args:
            args: Argumentos parseados (debe contener 'names').

        Returns:
            Código de salida.
        """
        people = args.names
        self.state.set_presence(people)

        print(f"✅ Presencia actualizada: {', '.join(people)}")
        return 0

    def cmd_presence_clear(self, args: argparse.Namespace) -> int:
        """
        Limpia la lista de personas presentes.

        Args:
            args: Argumentos parseados.

        Returns:
            Código de salida.
        """
        self.state.clear_presence()
        print("✅ Lista de presencia limpiada. No hay nadie en casa.")
        return 0


def create_parser() -> argparse.ArgumentParser:
    """
    Crea el parser de argumentos para la CLI.

    Returns:
        ArgumentParser configurado.
    """
    parser = argparse.ArgumentParser(
        prog='mcp-home-simulator',
        description='Simulador de sistema domótico con soporte MCP'
    )

    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Ruta al archivo de configuración (default: config.yaml)'
    )

    subparsers = parser.add_subparsers(
        dest='command', help='Comandos disponibles')

    # Comando: status
    subparsers.add_parser(
        'status', help='Muestra el estado general del sistema')

    # Comando: lights
    lights_parser = subparsers.add_parser('lights', help='Gestiona las luces')
    lights_subparsers = lights_parser.add_subparsers(dest='lights_command')

    lights_subparsers.add_parser(
        'list', help='Lista todas las luces y su estado')

    lights_on_parser = lights_subparsers.add_parser(
        'on', help='Enciende una luz')
    lights_on_parser.add_argument('name', help='Nombre de la luz')

    lights_off_parser = lights_subparsers.add_parser(
        'off', help='Apaga una luz')
    lights_off_parser.add_argument('name', help='Nombre de la luz')

    # Comando: alarm
    alarm_parser = subparsers.add_parser('alarm', help='Gestiona la alarma')
    alarm_subparsers = alarm_parser.add_subparsers(dest='alarm_command')

    alarm_subparsers.add_parser('on', help='Arma la alarma')
    alarm_subparsers.add_parser('off', help='Desarma la alarma')

    # Comando: presence
    presence_parser = subparsers.add_parser(
        'presence', help='Gestiona el detector de presencia')
    presence_subparsers = presence_parser.add_subparsers(
        dest='presence_command')

    presence_subparsers.add_parser(
        'show', help='Muestra el estado de presencia')

    presence_set_parser = presence_subparsers.add_parser(
        'set', help='Establece personas presentes')
    presence_set_parser.add_argument(
        'names', nargs='+', help='Nombres de las personas presentes')

    presence_subparsers.add_parser(
        'clear', help='Limpia la lista de personas presentes')

    return parser


def run_cli(args: Optional[List[str]] = None) -> int:
    """
    Ejecuta la interfaz CLI.

    Args:
        args: Argumentos de línea de comandos (None = usar sys.argv).

    Returns:
        Código de salida.
    """
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        return 1

    cli = CLI(parsed_args.config)

    # Despachar comandos
    if parsed_args.command == 'status':
        return cli.cmd_status(parsed_args)

    elif parsed_args.command == 'lights':
        if not parsed_args.lights_command:
            print("❌ Error: Especifica un subcomando para 'lights' (list, on, off)")
            return 1

        if parsed_args.lights_command == 'list':
            return cli.cmd_lights_list(parsed_args)
        elif parsed_args.lights_command == 'on':
            return cli.cmd_lights_on(parsed_args)
        elif parsed_args.lights_command == 'off':
            return cli.cmd_lights_off(parsed_args)

    elif parsed_args.command == 'alarm':
        if not parsed_args.alarm_command:
            print("❌ Error: Especifica un subcomando para 'alarm' (on, off)")
            return 1

        if parsed_args.alarm_command == 'on':
            return cli.cmd_alarm_on(parsed_args)
        elif parsed_args.alarm_command == 'off':
            return cli.cmd_alarm_off(parsed_args)

    elif parsed_args.command == 'presence':
        if not parsed_args.presence_command:
            print("❌ Error: Especifica un subcomando para 'presence' (show, set, clear)")
            return 1

        if parsed_args.presence_command == 'show':
            return cli.cmd_presence_show(parsed_args)
        elif parsed_args.presence_command == 'set':
            return cli.cmd_presence_set(parsed_args)
        elif parsed_args.presence_command == 'clear':
            return cli.cmd_presence_clear(parsed_args)

    print(f"❌ Error: Comando desconocido '{parsed_args.command}'")
    return 1
