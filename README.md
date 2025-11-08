# TPA-Grupo-a-Click-and-Hide

Repositorio de GitHub correspondiente al proyecto de Técnicas de Programación Avanzada (TPA). Este proyecto consiste en un juego tipo clicker llamado Click & Hide, desarrollado en Python utilizando Pygame para la gestión de la interfaz y la lógica del juego.

# Descripción del Juego

Click & Hide v.1.0.0 es un juego en el que el jugador puede hacer clic repetidamente para acumular dinero, comprar mejoras y desbloquear logros. El juego cuenta con un sistema de tienda donde se pueden adquirir ítems de tipo "click" y "auto", los cuales incrementan los ingresos manuales o pasivos del jugador respectivamente. Cada ítem aumenta su precio progresivamente para mantener el equilibrio del juego. Además, se incluyen logros que registran el progreso y proporcionan incentivos para continuar jugando.

# Miembros del grupo
- Miguel Angel Terol
- Alvaro Lacosta
- Guillermo Puertas
- Jaime Sanfeliciano
- David Lopez

# Registro de contribuciones
- Alvaro Lacosta - Implementacion de logros, menu, código.
- David Lopez - Implemetacion de la tienda y patrones de diseño creacionales.
- Miguel Angel Terol - Codigo base del programa, assets y documentación.
- Guillermo Puertas - venv, diagrama UML, HTML docs y código.
- Jaime San Feliciano - Interfaz grafica.

# Herramientas 
- Python 3.11+
- Pygame
- ChatGPT
- Docstrings
- PyDoc


# Ejecución
**Clonar el repositorio**
git clone https://github.com/alacostap/TPA-Grupo-a-Click-and-Hide.git
cd TPA-Grupo-a-Click-and-Hide

**Permitir la ejecución de scripts en PowerShell (solo la primera vez)**
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

**Crear y activar el entorno virtual**
python -m venv venv
venv\Scripts\activate

**Instalar dependencias**
pip install -r requirements.txt

**Ir a la carpeta del juego y ejecutar**
cd ClickAndHide
python main.py         # Ejecutar en modo normal
python main.py --demo  # Ejecutar en modo demo

**Desactivar el entorno virtual**
deactivate

# Documentos HTML
Clonar el repositorio (vease Ejecución)
Acceder a la carpeta "Docs_HTML"
Ejecutar cd.. si en la ruta TPA-Grupo-a-Click-and-Hide\ClickAndHide para acceder a TPA-Grupo-a-Click-and-Hide
Ejecutar cd "Docs_HTML"
Ejecutar start + nombre del archivo.
    Ejemplo: ``start main.html``