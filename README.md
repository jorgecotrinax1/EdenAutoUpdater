# Eden Emulator Auto Updater

![Windows](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)
![Python](https://img.shields.io/badge/Python-Required-3776AB?style=for-the-badge&logo=python)

Actualizador automático especializado para **Eden Nightly Emulator** exclusivo en Windows.

## 🚀 Características

- 🔍 **Detección automática** de nuevas versiones nightly
- 📥 **Descarga e instalación** con un solo clic
- 🏗️ **Soporte multi-arquitectura**: ARM64 y x86_64
- 📂 **Gestión inteligente** de ubicaciones del emulador
- 🚀 **Acceso directo** para abrir el emulador
- ⚡ **Interfaz simple** y fácil de usar

## 📋 Requisitos

- **Sistema Operativo**: Windows
- **Python**: Debe estar instalado en el sistema
- **Conexión a Internet**: Para descargar actualizaciones

## 🛠️ Instalación y Uso

1. **Preparación**
   ```bash
   # Crea una carpeta dedicada para el actualizador
   mkdir Eden-Updater
   cd Eden-Updater
   ```

2. **Coloca el archivo** `eden_updater.py` en la carpeta creada

3. **Ejecución**
   - Haz doble clic en `eden_updater.py`
   - O ejecuta desde línea de comandos:
     ```bash
     python eden_updater.py
     ```

4. **Configuración inicial**
   - Selecciona la carpeta donde está instalado tu emulador Eden
   - El programa creará automáticamente `eden_updater_config.json`

## 🎮 Cómo actualizar

1. **Verifica actualizaciones** - Comprueba si hay nuevas versiones disponibles
2. **Descarga y actualiza** - Instala la última versión nightly automáticamente
3. **Abre el emulador** - Inicia Eden con las últimas mejoras

## 📁 Estructura soportada

| Arquitectura | Formato del archivo |
|--------------|---------------------|
| **ARM64** | `Eden-*-arm64.7z` |
| **x86_64** | `Eden-*-x86_64.7z` |

## 🔗 Enlaces oficiales

- **Repositorio oficial**: [pflyly/eden-nightly](https://github.com/pflyly/eden-nightly)
- **Tipo de versiones**: Exclusivamente builds nightly

## 👨‍💻 Desarrollador

### 🌐 Sígueme en mis redes:

[![Discord](https://img.shields.io/badge/Discord-Join_Server-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/9UMawCFkbK)
[![YouTube](https://img.shields.io/badge/YouTube-Subscribe-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@jorgecotrinax8723)
[![Facebook](https://img.shields.io/badge/Facebook-Follow-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/ElNekocsm/)

## 💡 Notas importantes

- ⚠️ **Solo para Windows** - No compatible con otros sistemas operativos
- 📝 **Crea una carpeta dedicada** - El programa genera archivos de configuración
- 🔄 **Versiones nightly** - Actualiza solo con builds de desarrollo inestables

## 🖥️ Vista previa de la interfaz

```
Versión actual: v1.0.0
Última versión disponible: v1.1.0

Seleccionar Carpeta
Última carpeta: D:\Descargas\Eden

Release: 2025-11-18-28022
Arquitectura: ARM64 / x86_64

[Verificar Actualizaciones] [Descargar y Actualizar] [Abrir Emulador]
```

---

**Mantén tu emulador Eden siempre actualizado con las últimas mejoras nightly** 🎯

**¿Problemas o sugerencias?** Únete a nuestro [Discord](https://discord.gg/9UMawCFkbK) para soporte y actualizaciones.
