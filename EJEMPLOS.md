# MCP Home Simulator - Ejemplos de Uso

## Ejemplo 1: Secuencia CLI Completa

```bash
# 1. Ver estado inicial
python -m mcp_home_simulator status

# 2. Encender varias luces
python -m mcp_home_simulator lights on salon
python -m mcp_home_simulator lights on cocina

# 3. Listar luces encendidas
python -m mcp_home_simulator lights list

# 4. Establecer personas presentes
python -m mcp_home_simulator presence set Carlos Ana Juan

# 5. Verificar presencia
python -m mcp_home_simulator presence show

# 6. Armar la alarma
python -m mcp_home_simulator alarm on

# 7. Ver estado final
python -m mcp_home_simulator status

# 8. Apagar una luz
python -m mcp_home_simulator lights off cocina

# 9. Limpiar presencia
python -m mcp_home_simulator presence clear

# 10. Desarmar alarma
python -m mcp_home_simulator alarm off
```

## Ejemplo 2: Sesión MCP Interactiva

### Iniciar el servidor
```bash
python -m mcp_home_simulator --mcp
```

### Mensaje de bienvenida (servidor envía automáticamente):
```json
{
  "type": "ready",
  "version": "0.1.0",
  "tools": [
    {
      "name": "get_presence",
      "description": "Obtiene el estado del detector de presencia",
      ...
    },
    ...
  ]
}
```

### Enviar comandos (cliente → servidor):

**1. Obtener estado completo**
```json
{"type":"call","id":1,"tool":"get_all_states","args":{}}
```
Respuesta:
```json
{
  "type": "result",
  "id": 1,
  "ok": true,
  "result": {
    "lights": {"salon": false, "cocina": false, ...},
    "alarm": false,
    "presence": {"present": false, "known_people": []}
  }
}
```

**2. Encender una luz**
```json
{"type":"call","id":2,"tool":"set_light_state","args":{"name":"salon","on":true}}
```
Respuesta:
```json
{"type": "result", "id": 2, "ok": true, "result": {"ok": true}}
```

**3. Listar luces encendidas**
```json
{"type":"call","id":3,"tool":"list_lights_on","args":{}}
```
Respuesta:
```json
{"type": "result", "id": 3, "ok": true, "result": {"on": ["salon"]}}
```

**4. Armar la alarma**
```json
{"type":"call","id":4,"tool":"set_alarm_state","args":{"armed":true}}
```
Respuesta:
```json
{"type": "result", "id": 4, "ok": true, "result": {"ok": true}}
```

**5. Consultar estado de alarma**
```json
{"type":"call","id":5,"tool":"get_alarm_status","args":{}}
```
Respuesta:
```json
{"type": "result", "id": 5, "ok": true, "result": {"armed": true}}
```

**6. Obtener presencia**
```json
{"type":"call","id":6,"tool":"get_presence","args":{}}
```
Respuesta:
```json
{
  "type": "result",
  "id": 6,
  "ok": true,
  "result": {"present": false, "known_people": []}
}
```

**7. Intentar encender luz inexistente (error)**
```json
{"type":"call","id":7,"tool":"set_light_state","args":{"name":"inexistente","on":true}}
```
Respuesta:
```json
{
  "type": "error",
  "id": 7,
  "ok": false,
  "error": "Luz 'inexistente' no encontrada"
}
```

**8. Terminar sesión**
```json
{"type":"quit"}
```

## Ejemplo 3: Prueba desde PowerShell

```powershell
# Crear archivo de comandos
@"
{"type":"call","id":1,"tool":"set_light_state","args":{"name":"salon","on":true}}
{"type":"call","id":2,"tool":"set_light_state","args":{"name":"cocina","on":true}}
{"type":"call","id":3,"tool":"set_alarm_state","args":{"armed":true}}
{"type":"call","id":4,"tool":"get_all_states","args":{}}
"@ | Out-File -Encoding UTF8 commands.json

# Ejecutar
Get-Content commands.json | python -m mcp_home_simulator --mcp
```

## Ejemplo 4: Integración con Python

```python
import subprocess
import json

def call_mcp_tool(tool_name, args, msg_id=1):
    """Llama a una tool MCP del simulador."""
    message = {
        "type": "call",
        "id": msg_id,
        "tool": tool_name,
        "args": args
    }
    
    # Iniciar proceso MCP
    proc = subprocess.Popen(
        ["python", "-m", "mcp_home_simulator", "--mcp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Leer mensaje ready
    ready_line = proc.stdout.readline()
    ready_msg = json.loads(ready_line)
    print("Servidor listo, tools disponibles:", len(ready_msg['tools']))
    
    # Enviar comando
    proc.stdin.write(json.dumps(message) + "\n")
    proc.stdin.flush()
    
    # Leer respuesta
    response_line = proc.stdout.readline()
    response = json.loads(response_line)
    
    # Terminar proceso
    proc.stdin.write('{"type":"quit"}\n')
    proc.stdin.flush()
    proc.wait()
    
    return response

# Uso
if __name__ == "__main__":
    # Encender luz
    result = call_mcp_tool("set_light_state", {"name": "salon", "on": True}, 1)
    print("Resultado:", result)
    
    # Obtener estado
    result = call_mcp_tool("get_all_states", {}, 2)
    print("Estado completo:", json.dumps(result['result'], indent=2, ensure_ascii=False))
```

## Ejemplo 5: Caso de Uso Realista

### Escenario: "Modo Noche"

```bash
# 1. Alguien llega a casa
python -m mcp_home_simulator presence set Maria

# 2. Enciende luces necesarias
python -m mcp_home_simulator lights on salon
python -m mcp_home_simulator lights on cocina

# 3. Verifica que todo está bien
python -m mcp_home_simulator status

# 4. Hora de dormir - apagar luces comunes
python -m mcp_home_simulator lights off salon
python -m mcp_home_simulator lights off cocina

# 5. Encender luz del dormitorio
python -m mcp_home_simulator lights on dormitorio

# 6. Armar la alarma
python -m mcp_home_simulator alarm on

# 7. Estado final antes de dormir
python -m mcp_home_simulator status
```

### Salida esperada del último comando:
```
╔═══════════════════════════════════════════╗
║    ESTADO GENERAL DEL SISTEMA DOMÓTICO   ║
╚═══════════════════════════════════════════╝

🔆 LUCES:
  • salon: ⚫ Apagada
  • cocina: ⚫ Apagada
  • dormitorio: 🟢 Encendida
  • bano: ⚫ Apagada
  • garage: ⚫ Apagada

🚨 ALARMA: 🔴 ARMADA

👥 PRESENCIA: ✅ Hay personas
  Personas presentes: Maria
```

## Ejemplo 6: Manejo de Errores

```bash
# Intentar encender luz inexistente
python -m mcp_home_simulator lights on piscina

# Salida:
# ❌ Error: La luz 'piscina' no existe.
#    Luces disponibles: salon, cocina, dormitorio, bano, garage

# Intentar apagar luz ya apagada (no es error)
python -m mcp_home_simulator lights off salon

# Salida:
# ✅ Luz 'salon' apagada.
```

## Ejemplo 7: Configuración Personalizada

```yaml
# mi_casa.yaml
lights:
  - living
  - kitchen
  - bedroom1
  - bedroom2
  - bathroom
  - hallway
  - garden

alarm_default: true

presence_default:
  present: true
  known_people:
    - John
    - Jane
```

Usar configuración personalizada:
```bash
python -m mcp_home_simulator --config mi_casa.yaml status
```

---

**Nota**: Estos ejemplos asumen que cada comando se ejecuta de forma independiente. El estado no persiste entre ejecuciones en la versión actual (0.1.0).
