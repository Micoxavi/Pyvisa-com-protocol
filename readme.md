# 🔌 VISA Communication Toolkit

**Estado: En desarrollo 🚧 – Instrumentos funcionales ✅**

Este proyecto tiene como objetivo ofrecer una interfaz sencilla y extensible para comunicarte con instrumentos de laboratorio mediante protocolos compatibles con **VISA (Virtual Instrument Software Architecture)**, utilizando **PyVISA** como backend.

Aunque la herramienta aún **no está finalizada**, los scripts actuales permiten:
- 🧪 Comunicar con fuentes de alimentación, multímetros y dataloggers.
- 💾 Guardar datos en CSV.
- 🖥️ Probar dispositivos de forma independiente mediante scripts `*_test.py`.

---

## 📁 Estructura del proyecto

```
Visa_protocol/
├── csv_editor.py                # Módulo para guardar y leer CSVs
├── data_extractor.py           # GUI básica para extracción de datos
├── visa_comunication.py        # Gestión de conexión y escaneo de dispositivos
├── visa_instruments.py         # Clases específicas para cada tipo de instrumento
├── example_auto_test.py        # Script de prueba automático
├── pyvisa_multimeter_test.py  # Test de multímetro
├── pyvisa_power_supply_test.py# Test de fuente de alimentación
├── pyvisa_datalogger_test.py  # Test de datalogger
└── requirements.txt            # Dependencias (por completar)
```

---

## 🛠️ Requisitos

- Python 3.7+
- `pyvisa`
- `pyvisa-py`
- `numpy`
- `pyqt5` (para la GUI)

Instalación rápida (entorno virtual recomendado):

```bash
pip install -r requirements.txt
```

---

## 🚀 Cómo empezar

1. Crea un entorno virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Instala dependencias:
   ```bash
   pip install pyvisa pyvisa-py numpy pyqt5
   ```

3. Ejecuta un test:
   ```bash
   python pyvisa_power_supply_test.py
   ```

---

## 🧩 Estado del desarrollo

✅ Instrumentos funcionales  
🔄 Pendiente:
- Integración GUI con comunicación real
- Gestión de errores mejorada
- Documentación extendida

---

## 📬 Contribuciones

¡Son bienvenidas! El objetivo es dejar una base modular para cualquier entorno de laboratorio compatible con VISA.

---

## 📜 Licencia

Este proyecto está bajo licencia MIT.