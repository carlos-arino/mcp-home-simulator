# Roadmap - MCP Home Simulator

Este documento describe las mejoras y características planeadas para futuras versiones del proyecto.

## ✅ Versión 0.1.0 (Actual)

**Funcionalidades implementadas:**

- ✅ Configuración mediante `config.yaml`
- ✅ Gestión de luces (encender/apagar, listar)
- ✅ Sistema de alarma (armar/desarmar)
- ✅ Detector de presencia (consultar, establecer, limpiar)
- ✅ Interfaz CLI completa
- ✅ Servidor MCP por stdio
- ✅ 6 tools MCP principales
- ✅ Manejo de errores
- ✅ Documentación básica
- ✅ Tests unitarios básicos

## 🚀 Versión 0.2.0 (Planeada)

**Persistencia del estado:**

- [ ] Guardar estado en archivo JSON al modificar
- [ ] Cargar estado automáticamente al iniciar
- [ ] Opción `--no-persist` para modo temporal

**Mejoras en presencia:**

- [ ] Timestamp de entrada/salida para cada persona
- [ ] Historial de presencia (últimas N entradas)
- [ ] Tool `get_presence_history`

**Logging:**

- [ ] Sistema de logs configurable
- [ ] Niveles: DEBUG, INFO, WARNING, ERROR
- [ ] Opción `--log-level` en CLI y MCP

## 🔮 Versión 0.3.0 (Futuro)

**Nuevos dispositivos:**

- [ ] Termostato (temperatura objetivo, actual)
- [ ] Persianas (abrir/cerrar, porcentaje)
- [ ] Cámaras (estado, grabación)
- [ ] Sensores (temperatura, humedad, movimiento)

**Escenas:**

- [ ] Definir escenas en configuración (ej: "Noche", "Salir")
- [ ] Comando CLI: `scene activate noche`
- [ ] Tool MCP: `activate_scene`

**Automatizaciones:**

- [ ] Reglas simples basadas en estado
- [ ] Ejemplo: "Si no hay presencia y pasan 5 min → apagar todas las luces"

## 🌟 Versión 0.4.0 (Futuro)

**Interfaz web:**

- [ ] Dashboard web simple con Flask o FastAPI
- [ ] Control visual de todos los dispositivos
- [ ] Visualización de estado en tiempo real

**API REST:**

- [ ] Endpoints RESTful además de MCP
- [ ] Compatibilidad con Home Assistant
- [ ] Webhooks para eventos

**Simulación avanzada:**

- [ ] Modo "tiempo real" con eventos automáticos
- [ ] Simulación de consumo energético
- [ ] Estadísticas y gráficas

## 🎯 Versión 1.0.0 (Objetivo a largo plazo)

**Madurez del proyecto:**

- [ ] Cobertura de tests > 90%
- [ ] Documentación completa (API reference)
- [ ] Ejemplos de integración con LLMs populares
- [ ] Benchmarks de rendimiento

**Compatibilidad MCP completa:**

- [ ] Implementar MCP oficial (JSON-RPC 2.0)
- [ ] Soporte para notificaciones push
- [ ] Negociación de capacidades

**Empaquetado:**

- [ ] Publicar en PyPI
- [ ] Imágenes Docker
- [ ] Instaladores para Windows/Mac/Linux

## 💡 Ideas para Contribuciones

¿Te interesa contribuir? Aquí hay algunas ideas:

### Fácil (Good First Issue)

- [ ] Añadir más emojis personalizados en salidas CLI
- [ ] Traducir mensajes a inglés (i18n básico)
- [ ] Mejorar documentación con más ejemplos
- [ ] Añadir validación de tipos con mypy

### Intermedio

- [ ] Implementar persistencia de estado
- [ ] Añadir tests de integración
- [ ] Crear script de generación de configuración interactiva
- [ ] Añadir soporte para múltiples archivos de configuración

### Avanzado

- [ ] Implementar interfaz web
- [ ] Soporte para plugins/extensiones
- [ ] Compatibilidad con protocolo MCP oficial
- [ ] Sistema de automatizaciones con DSL

## 📝 Notas

- Las versiones son orientativas y pueden cambiar según feedback
- Las funcionalidades en roadmap no garantizan implementación
- Las contribuciones son bienvenidas para acelerar el desarrollo

## 🤝 Cómo Proponer Nuevas Características

1. Abre un **Issue** en GitHub con la etiqueta `feature-request`
2. Describe el caso de uso y beneficio esperado
3. Si es posible, incluye un ejemplo de cómo se usaría
4. La comunidad votará y discutirá la propuesta

---

**Última actualización**: 2025-12-17  
**Versión actual**: 0.1.0
