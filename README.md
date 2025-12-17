# MCP Home Simulator

Simulador de sistema domótico compatible con **Model Context Protocol (MCP)** que permite controlar luces, alarma y detector de presencia tanto por **línea de comandos (CLI)** como por **stdio** (para integración con IA).

## 🏠 Características

- **Luces configurables**: Define tus propias luces en `config.yaml`
- **Sistema de alarma**: Arma y desarma la alarma
- **Detector de presencia**: Rastrea quién está en casa
- **Doble interfaz**:
  - **CLI**: Comandos interactivos por terminal
  - **MCP stdio**: Protocolo JSON para integración con IA

## 📦 Instalación

### Desde el código fuente

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/mcp-home-simulator.git
cd mcp-home-simulator

# Instalar en modo desarrollo
pip install -e .

# O instalar con dependencias de desarrollo
pip install -e ".[dev]"
```

### Requisitos

- Python 3.8 o superior
- pyyaml

 ### Configuración

 Edita `config.yaml`:

 ```yaml
 lights:
   - salon
   - cocina
   - dormitorio
 alarm_default: false
 presence_default:
   present: false
   known_people: []
 ```

 ### Uso (CLI)

 ```bash
 python -m mcp_home_simulator status
 python -m mcp_home_simulator lights list
 python -m mcp_home_simulator lights on salon
 python -m mcp_home_simulator alarm on
 python -m mcp_home_simulator presence set Carlos Ana
 python -m mcp_home_simulator presence show
 ```

 ### Uso (MCP por stdio)

 ```bash
 python -m mcp_home_simulator --mcp=stdio
 ```

 Envía por `stdin`:

 ```json
 {"type":"call","id":1,"tool":"get_alarm_status","args":{}}
 ```

 Respuesta (stdout):

 ```json
 {"type":"result","id":1,"ok":true,"result":{"armed":false}}
 ```

 ### Tools MCP disponibles

 *   `get_presence` → `{ present: bool, known_people: [string] }`
 *   `get_alarm_status` → `{ armed: bool }`
 *   `list_lights_on` → `{ on: [string] }`
 *   `set_light_state` → entrada `{ name: string, on: bool }`, salida `{ ok: bool }`
 *   `set_alarm_state` → entrada `{ armed: bool }`, salida `{ ok: bool }`
 *   `get_all_states` → snapshot completo.

 ### Notas

 *   Protocolo MCP **simplificado** para pruebas (ver `docs/protocol.md`).
 *   No controla hardware real; **simulación** en memoria.
