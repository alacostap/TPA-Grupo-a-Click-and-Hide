"""
config.py — Archivo de configuración global para el juego Click & Hide.
Contiene constantes relacionadas con:
  - Pantalla
  - Jugador
  - Colores
  - Fuentes
  - Rutas de recursos
  - Parámetros de la intro
  - Depuración / desarrollo
"""

# --- CONFIGURACIÓN DE PANTALLA ---
WIDTH = 1280          # Ancho de la ventana
HEIGHT = 720          # Alto de la ventana
FPS = 60              # Frames por segundo
FULLSCREEN = False    # Si True, pantalla completa

# --- PARÁMETROS DEL JUGADOR ---
MONEY_START = 0       # Dinero inicial
EARN_AMOUNT = 1       # Dinero por clic
EARN_COOLDOWN = 0.2   # Tiempo mínimo entre clics que dan dinero

# --- COLORES GENERALES (RGB) ---
COLOR_BG_TOP = (250, 240, 210)     # Fondo superior (gradiente)
COLOR_BG_BOTTOM = (235, 220, 180)  # Fondo inferior (gradiente)
COLOR_HEADER = (180, 150, 100)     # Encabezado superior
COLOR_PANEL = (245, 240, 220)      # Paneles
COLOR_TEXT = (50, 35, 20)          # Texto general

# --- PARÁMETROS DE LA TIENDA ---
SHOP_PANEL_WIDTH = 380     # Ancho del panel de la tienda
SHOP_ITEM_HEIGHT = 60      # Altura de cada ítem
SHOP_PADDING_X = 30        # Espaciado horizontal
SHOP_PADDING_Y = 8         # Espaciado vertical

# --- CONFIGURACIÓN DE FUENTES ---
FONT_PATH = "assets/fonts/PressStart2P.ttf"  # Ruta de la fuente principal
FONT_SMALL = 14
FONT_MEDIUM = 18
FONT_BIG = 28

# --- INTRO / PANTALLA DE PRESENTACIÓN ---
INTRO_IMAGE = "clase.png"           # Fondo de la intro
LOGO_SIZE = (100, 100)              # Tamaño del logo
INTRO_MOVE_DURATION = 3.0           # Tiempo del movimiento del texto
INTRO_LOAD_DURATION = 5.0           # Tiempo de carga
INTRO_FONT_SIZE = 64                # Tamaño del texto principal
INTRO_TEXT = "CLICK AND HIDE"       # Texto principal de la intro
INTRO_TEXT_COLOR = (255, 255, 255)  # Color del texto principal

# --- RUTAS Y ARCHIVOS ---
ASSETS_PATH = "assets"
IMAGES_PATH = f"{ASSETS_PATH}/images"
FONTS_PATH = f"{ASSETS_PATH}/fonts"
SOUNDS_PATH = f"{ASSETS_PATH}/sounds"

# --- DEBUG / DESARROLLO ---
DEBUG_MODE = False
