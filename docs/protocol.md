# Especificación del Protocolo MCP Simplificado

Este documento describe el protocolo de comunicación MCP (Model Context Protocol) utilizado por el simulador de domótica. Es una implementación simplificada que usa **mensajes JSON line-delimited** por `stdin/stdout`.

## Visión General

- **Transporte**: stdio (standard input/output)
- **Formato**: JSON, un mensaje por línea
- **Codificación**: UTF-8
- **Dirección**: Bidireccional (cliente envía `call`, servidor responde `result`)

## Flujo de Comunicación

```
Cliente                    Servidor
  |                           |
  |  (inicia servidor)        |
  |<------------------------- | mensaje "ready" con lista de tools
  |                           |
  |  {"type":"call",...}      |
  |-------------------------->| procesa llamada
  |                           |
  |  {"type":"result",...}    |
  |<------------------------- | devuelve resultado
  |                           |
  |  {"type":"call",...}      |
  |-------------------------->| otra llamada
  |                           |
  |  {"type":"error",...}     |
  |<------------------------- | error en la operación
  |                           |
```

## Tipos de Mensajes

### 1. Mensaje `ready` (Servidor → Cliente)

Enviado al inicio por el servidor para anunciar las tools disponibles.

**Formato:**

```json
{
  "type": "ready",
  "version": "0.1.0",
  "tools": [
    {
      "name": "get_presence",
      "description": "Obtiene el estado del detector de presencia",
      "input_schema": {
        "type": "object",
        "properties": {},
        "required": []
      },
      "output_schema": {
        "type": "object",
        "properties": {
          "present": {"type": "boolean"},
          "known_people": {"type": "array", "items": {"type": "string"}}
        }
      }
    },
    ...
  ]
}
```

**Campos:**

- `type`: Siempre `"ready"`
- `version`: Versión del protocolo/servidor
- `tools`: Array con la definición de cada tool disponible

### 2. Mensaje `call` (Cliente → Servidor)

Solicita la ejecución de una tool.

**Formato:**

```json
{
  "type": "call",
  "id": 1,
  "tool": "set_light_state",
  "args": {
    "name": "salon",
    "on": true
  }
}
```

**Campos:**

- `type`: Siempre `"call"`
- `id`: Identificador único del mensaje (número o string)
- `tool`: Nombre de la tool a ejecutar
- `args`: Diccionario con los argumentos de entrada

### 3. Mensaje `result` (Servidor → Cliente)

Respuesta exitosa a una llamada.

**Formato:**

```json
{
  "type": "result",
  "id": 1,
  "ok": true,
  "result": {
    "ok": true
  }
}
```

**Campos:**

- `type`: Siempre `"result"`
- `id`: Mismo ID que el mensaje `call` original
- `ok`: Siempre `true` en un resultado exitoso
- `result`: Datos de respuesta de la tool

### 4. Mensaje `error` (Servidor → Cliente)

Indica que hubo un error al procesar la llamada.

**Formato:**

```json
{
  "type": "error",
  "id": 1,
  "ok": false,
  "error": "Luz 'inexistente' no encontrada"
}
```

**Campos:**

- `type`: Siempre `"error"`
- `id`: ID del mensaje `call` original (puede ser `null` si el error fue de parsing)
- `ok`: Siempre `false`
- `error`: Descripción del error en texto

### 5. Mensaje `quit` (Cliente → Servidor)

Opcional. Indica al servidor que debe terminar el bucle.

**Formato:**

```json
{
  "type": "quit"
}
```

## Tools Disponibles

### `get_presence`

Obtiene el estado del detector de presencia.

**Input:**
```json
{}
```

**Output:**
```json
{
  "present": true,
  "known_people": ["Carlos", "Ana"]
}
```

---

### `get_alarm_status`

Consulta si la alarma está armada.

**Input:**
```json
{}
```

**Output:**
```json
{
  "armed": true
}
```

---

### `list_lights_on`

Lista los nombres de las luces que están encendidas.

**Input:**
```json
{}
```

**Output:**
```json
{
  "on": ["salon", "cocina"]
}
```

---

### `set_light_state`

Enciende o apaga una luz específica.

**Input:**
```json
{
  "name": "salon",
  "on": true
}
```

**Output (éxito):**
```json
{
  "ok": true
}
```

**Output (error):**
```json
{
  "ok": false,
  "error": "Luz 'inexistente' no encontrada"
}
```

---

### `set_alarm_state`

Arma o desarma la alarma.

**Input:**
```json
{
  "armed": true
}
```

**Output:**
```json
{
  "ok": true
}
```

---

### `get_all_states`

Obtiene un snapshot completo del estado del sistema.

**Input:**
```json
{}
```

**Output:**
```json
{
  "lights": {
    "salon": true,
    "cocina": false,
    "dormitorio": false,
    "bano": false,
    "garage": true
  },
  "alarm": true,
  "presence": {
    "present": true,
    "known_people": ["Carlos", "Ana"]
  }
}
```

## Manejo de Errores

### Errores comunes

1. **Tool no encontrada**:
   ```json
   {
     "type": "error",
     "id": 1,
     "ok": false,
     "error": "Tool 'tool_inexistente' no encontrada"
   }
   ```

2. **Luz no encontrada**:
   ```json
   {
     "type": "error",
     "id": 2,
     "ok": false,
     "error": "Luz 'dormitorio2' no encontrada"
   }
   ```

3. **Error de parsing JSON**:
   ```json
   {
     "type": "error",
     "id": null,
     "ok": false,
     "error": "Error al parsear JSON: Expecting value: line 1 column 1 (char 0)"
   }
   ```

4. **Parámetros faltantes**:
   ```json
   {
     "type": "error",
     "id": 3,
     "ok": false,
     "error": "Faltan parámetros requeridos: name, on"
   }
   ```

## Ejemplo de Sesión Completa

```bash
# Iniciar servidor
$ python -m mcp_home_simulator --mcp
```

**Servidor envía (stdout):**
```json
{"type":"ready","version":"0.1.0","tools":[...]}
```

**Cliente envía (stdin):**
```json
{"type":"call","id":1,"tool":"set_light_state","args":{"name":"salon","on":true}}
```

**Servidor responde (stdout):**
```json
{"type":"result","id":1,"ok":true,"result":{"ok":true}}
```

**Cliente envía (stdin):**
```json
{"type":"call","id":2,"tool":"get_all_states","args":{}}
```

**Servidor responde (stdout):**
```json
{"type":"result","id":2,"ok":true,"result":{"lights":{"salon":true,"cocina":false,...},"alarm":false,"presence":{"present":false,"known_people":[]}}}
```

**Cliente envía (stdin):**
```json
{"type":"call","id":3,"tool":"set_light_state","args":{"name":"inexistente","on":true}}
```

**Servidor responde (stdout):**
```json
{"type":"error","id":3,"ok":false,"error":"Luz 'inexistente' no encontrada"}
```

## Notas de Implementación

### Para Clientes

- Enviar **un mensaje JSON por línea** (terminado con `\n`)
- Incluir siempre un `id` único por cada `call`
- Parsear respuestas línea por línea
- Verificar `ok` en la respuesta para detectar errores

### Para Servidores

- Enviar `ready` inmediatamente al iniciar
- Procesar mensajes línea por línea
- Siempre incluir el `id` original en respuestas
- Usar `type: "error"` para todos los fallos

## Diferencias con MCP Oficial

Este es un protocolo **simplificado** para propósitos de prueba. Diferencias con el MCP oficial:

1. **Line-delimited JSON** en lugar de JSON-RPC 2.0
2. Sin soporte para notificaciones push del servidor
3. Sin mecanismo de reintentos o acknowledgements
4. Sin negociación de capacidades
5. Schemas simplificados

## Extensibilidad

Puedes añadir nuevas tools editando:

1. `tools.py`: Añadir método de implementación y registro
2. `state.py`: Si necesitas nuevo estado
3. Este documento: Documentar la nueva tool

---

**Versión del protocolo**: 0.1.0  
**Última actualización**: 2025-12-17
