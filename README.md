 **MCP Home Simulator (Python)**  
 Simulador de domótica con luces configurables, alarma y detector de presencia, accesible por **terminal** y por **MCP (stdio)**.

 ### Instalación

 ```bash
 python -m venv .venv
 source .venv/bin/activate  # en Windows: .venv\\Scripts\\activate
 pip install -e .
 ```

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
